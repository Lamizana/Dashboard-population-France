import re
import pandas as pd
from pathlib import Path
from utils.logger import Logger

LOG = Logger("deces_pipeline.log")


# ---------------------------------------------------------------------
def lire_fichier_deces(fichier: Path) -> pd.DataFrame:
    """
    Lecture d’un fichier texte de décès (INSEE) au format FWF.
    Extraction des colonnes à l’aide d’une expression régulière.
    """

    LOG.info(f"Lecture du fichier décès brut : {fichier}")
    lignes = []

    try:
        with open(fichier, "r", encoding="utf-8", errors="ignore") as f:
            for ligne in f:
                match = re.match(
                    r"^([A-ZÉÈÀÙÂÊÎÔÛÄËÏÖÜÇ' \-\*]+)/(?:\s*)(1|2)(\d{8})(\d{5})([A-Z \-']+)(\d{8})(\d{5})",
                    ligne
                )
                if match:
                    lignes.append(match.groups())

        colonnes = [
            "nom",
            "sexe",
            "date_naissance",
            "lieu_naissance_code",
            "lieu_naissance_nom",
            "date_deces",
            "lieu_deces_code",
        ]

        df = pd.DataFrame(lignes, columns=colonnes)
        LOG.info(f"{len(df):,} lignes lues depuis {fichier}")
        return df

    except Exception as e:
        LOG.error(f"Erreur lors de la lecture du fichier : {e}")
        raise


# ---------------------------------------------------------------------
def nettoyer_deces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyage du DataFrame : conversion des dates, calcul de l'âge,
    filtrage des valeurs aberrantes.
    """

    LOG.info("Nettoyage du DataFrame décès...")
    try:
        # Conversion des dates
        df["date_naissance"] = pd.to_datetime(df["date_naissance"], format="%Y%m%d", errors="coerce")
        df["date_deces"] = pd.to_datetime(df["date_deces"], format="%Y%m%d", errors="coerce")

        # Calcul de l'âge au décès
        df["age_deces"] = ((df["date_deces"] - df["date_naissance"]).dt.days / 365.25).round(0)

        # Filtrage des âges aberrants
        df.loc[(df["age_deces"] < 0) | (df["age_deces"] > 140), "age_deces"] = pd.NA

        LOG.info("✅ Nettoyage terminé avec succès.")
        return df

    except Exception as e:
        LOG.error(f"Erreur pendant le nettoyage : {e}")
        raise


# ---------------------------------------------------------------------
def convertir_deces_txt_en_csv(year: int) -> pd.DataFrame:
    """
    Si le CSV n’existe pas encore, convertit le fichier texte en CSV.
    Si le CSV existe, le charge directement.
    """

    base_path = Path("dashboard/assets/data/deces")
    base_path.mkdir(parents=True, exist_ok=True)

    txt_path = base_path / f"deces-{year}.txt"
    csv_path = base_path / f"deces-{year}.csv"

    # Si le CSV existe déjà → lecture directe
    if csv_path.exists():
        LOG.info(f"✅ Fichier CSV déjà présent, chargement : {csv_path}")
        return pd.read_csv(csv_path)

    # Sinon, conversion à partir du fichier texte
    if not txt_path.exists():
        LOG.error(f"❌ Fichier texte introuvable : {txt_path}")
        raise FileNotFoundError(f"Fichier {txt_path} non trouvé.")

    LOG.info(f"📥 Conversion du fichier texte en CSV : {txt_path}")
    df = lire_fichier_deces(txt_path)
    df = nettoyer_deces(df)

    # Export CSV
    df.to_csv(csv_path, index=False, encoding="utf-8")
    LOG.info(f"💾 Fichier CSV enregistré : {csv_path}")

    return df


# ---------------------------------------------------------------------
def charger_deces(year: int = 2024) -> pd.DataFrame:
    """
    Fonction principale : charge les données de décès.
    - Si le CSV existe → lecture directe.
    - Sinon → conversion depuis le .txt, puis lecture.
    """

    try:
        LOG.info(f"Chargement des données de décès pour l’année {year}...")
        df = convertir_deces_txt_en_csv(year)
        LOG.info(f"✅ Données de décès {year} prêtes ({len(df):,} lignes)")
        return df
    except Exception as e:
        LOG.critical(f"Erreur fatale dans le pipeline décès : {e}")
        raise
