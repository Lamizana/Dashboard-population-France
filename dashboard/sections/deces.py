import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.data_loader import charger_parquet_multi

# ---------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    """Cache les données Parquet pour éviter le rechargement complet à chaque interaction."""
    data_dir = Path("data_processed/deces")
    return charger_parquet_multi(data_dir)

# ---------------------------------------------------------------------
def render():
    st.header("📊 Décès — Analyse interactive (Plotly)")
    st.caption("Source : INSEE / data.gouv.fr")

    df = load_data()
    if df.empty:
        st.warning("Aucune donnée chargée. Vérifie le dossier `data_processed/deces`.")
        return

    # Nettoyage / typage
    df = df.dropna(subset=["age_deces", "sexe", "annee_deces"])
    df["annee_deces"] = df["annee_deces"].astype(int)
    df["sexe"] = df["sexe"].astype(str)
    df = df[(df["annee_deces"] >= 2020) & (df["annee_deces"] <= 2024)]

    # --- Sidebar ---
    st.sidebar.subheader("Filtres décès")
    annees = sorted(df["annee_deces"].unique())
    annees_sel = st.sidebar.multiselect("Années", annees, default=annees)
    sexes = sorted(df["sexe"].unique())
    sexe_sel = st.sidebar.multiselect("Sexes", sexes, default=sexes)

    # Slider d’âge
    age_min, age_max = int(df["age_deces"].min()), int(df["age_deces"].max())
    age_range = st.sidebar.slider("Tranche d’âge", 0, 110, (0, 100))

    # Filtrage dynamique
    filtre = df[
        (df["annee_deces"].isin(annees_sel)) &
        (df["sexe"].isin(sexe_sel)) &
        (df["age_deces"].between(age_range[0], age_range[1]))
    ]

    # Échantillonnage pour performance
    sample_size = st.sidebar.slider("Taille d’échantillon max", 50_000, 500_000, 200_000, step=50_000)
    if len(filtre) > sample_size:
        filtre = filtre.sample(sample_size, random_state=42)
        st.info(f"⚠️ Sous-échantillonnage : {sample_size:,} enregistrements affichés sur {len(df):,} disponibles.")

    st.write(f"🧾 {len(filtre):,} enregistrements affichés (années {min(annees_sel)}–{max(annees_sel)})")

    # -----------------------------------------------------------------
    # 1️⃣ Histogramme des âges au décès
    st.subheader("Répartition de l'âge au décès")
    fig_age = px.histogram(
        filtre,
        x="age_deces",
        nbins=60,
        color_discrete_sequence=["#1f77b4"],
        title="Distribution de l'âge au décès",
        labels={"age_deces": "Âge au décès"},
    )
    fig_age.update_layout(bargap=0.05, xaxis_title="Âge", yaxis_title="Nombre de décès")
    st.plotly_chart(fig_age, use_container_width=True)

    # -----------------------------------------------------------------
    # 2️⃣ Évolution annuelle
    st.subheader("Évolution du nombre de décès par année et par sexe")
    fig_year = px.histogram(
        filtre,
        x="annee_deces",
        color="sexe",
        barmode="group",
        title="Décès par année et par sexe (2020–2024)",
        labels={"annee_deces": "Année de décès", "sexe": "Sexe"},
        color_discrete_map={"1": "steelblue", "2": "salmon"},
    )
    st.plotly_chart(fig_year, use_container_width=True)

    # -----------------------------------------------------------------
    # 3️⃣ Distribution âge/sexe (boxplot)
    st.subheader("Distribution de l’âge au décès par sexe")
    fig_box = px.box(
        filtre,
        x="sexe",
        y="age_deces",
        color="sexe",
        points="all",
        color_discrete_map={"1": "steelblue", "2": "salmon"},
        title="Distribution âge au décès par sexe"
    )
    fig_box.update_layout(yaxis_title="Âge au décès", xaxis_title="Sexe")
    st.plotly_chart(fig_box, use_container_width=True)

    # -----------------------------------------------------------------
    # 4️⃣ Saisonnalité mensuelle
    if "mois_deces" in filtre.columns:
        st.subheader("Saisonnalité des décès (par mois)")
        fig_month = px.histogram(
            filtre,
            x="mois_deces",
            color="sexe",
            barmode="stack",
            nbins=12,
            labels={"mois_deces": "Mois de décès", "sexe": "Sexe"},
            title="Décès par mois et par sexe (2020–2024)",
            color_discrete_map={"1": "steelblue", "2": "salmon"},
        )
        st.plotly_chart(fig_month, use_container_width=True)

    # -----------------------------------------------------------------
    # 5️⃣ Échantillon brut
    with st.expander("Voir un échantillon de données (1000 lignes)"):
        st.dataframe(filtre.head(1000), use_container_width=True)
