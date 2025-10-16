import streamlit as st
import plotly.express as px
from pathlib import Path
import pandas as pd

from utils.loader import charger_parquet_multi


# ---------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def list_available_years():
    """Liste toutes les années disponibles dans le dossier Parquet."""
    data_dir = Path("data_processed/deces")
    files = sorted(data_dir.glob("deces_*.parquet"))
    years = [int(f.stem.split("_")[1]) for f in files if f.stem.split("_")[1].isdigit()]
    return years, data_dir


# ---------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data_by_years(selected_years, base_dir):
    """Charge uniquement les années sélectionnées."""
    dfs = []
    for year in selected_years:
        path = base_dir / f"deces_{year}.parquet"
        if path.exists():
            df = pd.read_parquet(path)
            df["annee_deces"] = int(year)
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


# ---------------------------------------------------------------------
def render():
    st.header("📊 Décès — Analyse interactive")
    st.caption("Source : INSEE / data.gouv.fr")

    # === Charger la liste des années disponibles ===
    years, data_dir = list_available_years()
    if not years:
        st.error("Aucun fichier Parquet trouvé dans data_processed/deces/")
        return

    # --- Sidebar ---
    st.sidebar.subheader("Filtres décès")
    selected_years = st.sidebar.multiselect(
        "Sélectionne une ou plusieurs années", years, default=[max(years)]
    )

    if not selected_years:
        st.warning("Sélectionne au moins une année.")
        return

    # === Chargement ciblé des fichiers ===
    df = load_data_by_years(selected_years, data_dir)
    if df.empty:
        st.warning("Aucune donnée chargée pour ces années.")
        return

    # === Nettoyage rapide ===
    df = df.dropna(subset=["age_deces", "sexe", "annee_deces"])
    df["sexe"] = df["sexe"].astype(str)

    # === Autres filtres ===
    sexes = sorted(df["sexe"].unique())
    sexe_sel = st.sidebar.multiselect("Sexes", sexes, default=sexes)
    age_min, age_max = int(df["age_deces"].min()), int(df["age_deces"].max())
    age_range = st.sidebar.slider("Tranche d’âge", 0, 150, (0, 155))

    filtre = df[
        (df["sexe"].isin(sexe_sel)) &
        (df["age_deces"].between(age_range[0], age_range[1]))
    ]

    st.success(f"✅ {len(filtre):,} lignes chargées depuis {len(selected_years)} année(s).")

    # -----------------------------------------------------------------
    # 📊 Histogramme âge
    st.subheader("Répartition de l'âge au décès")
    fig_age = px.histogram(
        filtre,
        x="age_deces",
        nbins=80,
        color="sexe",
        barmode="overlay",
        color_discrete_map={"1": "DodgerBlue", "2": "LightCoral"},
        title=f"Distribution de l'âge au décès ({min(selected_years)}–{max(selected_years)})"
    )
    st.plotly_chart(fig_age, use_container_width=True)

    # -----------------------------------------------------------------
    # 📈 Décès par mois et par sexe
    st.subheader("Nombre de décès par mois et par sexe")

    if "mois_deces" in filtre.columns and "annee_deces" in filtre.columns:
        # Créer un identifiant unique "année-mois" pour l’axe X
        filtre["annee_mois"] = (
                filtre["annee_deces"].astype(str) + "-" + filtre["mois_deces"].astype(int).astype(str).str.zfill(2)
        )

        # Agréger le nombre de décès par mois et sexe
        data_mois = (
            filtre.groupby(["annee_mois", "sexe"], as_index=False)
                .size()
                .rename(columns={"size": "nb_deces"})
        )

        # Créer un histogramme Plotly
        fig_mois = px.bar(
            data_mois,
            x="annee_mois",
            y="nb_deces",
            color="sexe",
            barmode="group",  # ou "stack" selon préférence
            color_discrete_map={"1": "DodgerBlue", "2": "LightCoral"},
            title="Nombre de décès par mois et par sexe (2020–2024)",
            labels={"annee_mois": "Mois", "nb_deces": "Nombre de décès", "sexe": "Sexe"}
        )

        # Mise en forme de l’axe
        fig_mois.update_layout(
            xaxis_title="Période (AAAA-MM)",
            yaxis_title="Décès mensuels",
            xaxis_tickangle=-45,
            bargap=0.05,
            hovermode="x unified"
        )

        st.plotly_chart(fig_mois, use_container_width=True)

    else:
        st.warning("Les colonnes 'annee_deces' et 'mois_deces' sont nécessaires pour cette visualisation.")

    # -----------------------------------------------------------------
    # 📦 Boxplot âge/sexe
    st.subheader("Distribution de l’âge au décès par sexe")
    fig_box = px.box(
        filtre,
        x="sexe",
        y="age_deces",
        color="sexe",
        color_discrete_map={"1": "DodgerBlue", "2": "LightCoral"},
        points=False,
        title="Distribution de l’âge au décès par sexe"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # -----------------------------------------------------------------
    # 📅 Saisonnalité mensuelle explicite
    if "mois_deces" in filtre.columns:
        st.subheader("📅 Saisonnalité mensuelle des décès (2020–2024)")
        st.caption("Analyse de la répartition des décès selon les mois de l'année — toutes années confondues.")

        # Noms des mois en français
        mois_labels = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
            5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        filtre["mois_nom"] = filtre["mois_deces"].astype(int).map(mois_labels)

        # Ordre chronologique
        ordre_mois = list(mois_labels.values())
        filtre["mois_nom"] = pd.Categorical(filtre["mois_nom"], categories=ordre_mois, ordered=True)

        # Histogramme des décès par mois et sexe
        fig_month = px.histogram(
            filtre,
            x="mois_nom",
            color="sexe",
            barmode="stack",
            category_orders={"mois_nom": ordre_mois},
            color_discrete_map={"1": "DodgerBlue", "2": "LightCoral"},
            labels={"mois_nom": "Mois de décès", "sexe": "Sexe"},
            title="Répartition mensuelle des décès par sexe (2020–2024)"
        )

        fig_month.update_layout(
            xaxis_title="Mois de l'année",
            yaxis_title="Nombre total de décès",
            bargap=0.05,
            hovermode="x unified",
            legend_title="Sexe",
            xaxis_tickangle=-30,
        )

        st.plotly_chart(fig_month, use_container_width=True)

        # Commentaire contextuel
        st.markdown(
            """
            🔍 **Interprétation :**
            - Aucune pour le moment ...
            """
        )
    else:
        st.warning("Les colonnes 'mois_deces' sont nécessaires pour l'analyse de saisonnalité.")

    # -----------------------------------------------------------------
    # 📋 Échantillon de données
    with st.expander("Voir un aperçu des données"):
        st.dataframe(filtre.head(1000), use_container_width=True)
