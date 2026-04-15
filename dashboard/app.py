import streamlit as st
from sections import population, naissance, deces, viols, feminicides

st.set_page_config(
    page_title="Dashboard Population France",
    page_icon="🇫🇷",
    layout="wide"
)

st.title("Analyse de la population francaise")

# --- Barre latérale ---
section = st.sidebar.radio(
    "📂 Choisissez une section :",
    ["Population", "Naissance", "Décès", "Viols", "Féminicides"]
)

# --- Navigation ---
if section == "Décès":
    deces.render()
# elif section == "Naissance":
  # naissance.render()


# if section == "Population":
# population.show()
#elif section == "Naissance":
   # naissance.show()

#elif section == "Viols":
#    viols.show()
#elif section == "Féminicides":
  #  feminicides.show()

st.markdown("---")
st.caption("Source : data.gouv.fr | INSEE | Ministère de l'Intérieur  — © 2025 Alex LAMIZANA")
