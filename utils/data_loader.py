import os
import re
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from utils.logger import Logger

LOG = Logger()

# ---------------------------------------------------------------------
def lire_fichier_deces(fichier: Path) -> pd.DataFrame:
    """
    Lecture du fichier décès INSEE au format FWF (largeur fixe)
    """
    LOG.info(f"Lecture du fichier décès brut : {fichier}")

    if not fichier.exists():
        raise FileNotFoundError(f"Fichier non trouvé : {fichier}")

    colspecs = [
        (0, 80),        # nom + prénom
        (80, 81),       # sexe
        (81, 89),       # date naissance AAAAMMJJ
        (89, 94),       # code lieu naissance
        (94, 124),      # commune naissance
        (124, 154),     # pays naissance
        (154, 162),     # date décès AAAAMMJJ
        (162, 167),     # code lieu décès
        (167, 176)      # numéro d’acte
    ]
    names = [
        "nom_prenom",
        "sexe",
        "date_naissance",
        "code_lieu_naissance",
        "commune_naissance",
        "pays_naissance",
        "date_deces",
        "code_lieu_deces",
        "numero_acte"
    ]

    df = pd.read_fwf(fichier, colspecs=colspecs, names=names, dtype=str, encoding="utf-8")
    LOG.info(f"{len(df):_} lignes lues depuis {fichier}")
    return df


# ---------------------------------------------------------------------
def nettoyer_deces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et enrichit un DataFrame de décès :
    - Conversion des dates en datetime
    - Calcul de l’âge au décès
    - Filtrage des âges aberrants
    """

    LOG.info("Nettoyage des données de décès...")
    try:
        # Conversion des dates
        df["date_naissance"] = pd.to_datetime(df["date_naissance"], format="%Y%m%d", errors="coerce")
        df["date_deces"] = pd.to_datetime(df["date_deces"], format="%Y%m%d", errors="coerce")

        # Calcul de l'âge
        df["age_deces"] = ((df["date_deces"] - df["date_naissance"]).dt.days / 365.25).round(1)
        df.loc[(df["age_deces"] < 0) | (df["age_deces"] > 140), "age_deces"] = pd.NA

        # Ajout de colonnes dérivées utiles
        df["annee_deces"] = df["date_deces"].dt.year
        df["mois_deces"] = df["date_deces"].dt.month

        LOG.info("✅ Nettoyage terminé.")
        return df

    except Exception as e:
        LOG.error(f"Erreur pendant le nettoyage : {e}")
        raise


# ---------------------------------------------------------------------
def convert_to_parquet(
    source_dir: Path,
    output_dir: None,
    delete_original: bool = False,
):
    """
    Convertit tous les fichiers `.txt` d’un dossier en `.parquet` optimisés.

    Args:
        source_dir (Path): dossier contenant les fichiers texte
        output_dir (Path | None): dossier de sortie (par défaut = source_dir)
        delete_original (bool): supprime le fichier source après conversion si True
    """

    output_dir = output_dir or source_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    fichiers_txt = list(source_dir.glob("*.txt"))
    if not fichiers_txt:
        LOG.warning(f"Aucun fichier .txt trouvé dans {source_dir}")
        return

    LOG.info(f"Conversion de {len(fichiers_txt)} fichiers TXT → Parquet...")

    for f in tqdm(fichiers_txt, desc="Conversion en cours", unit="fichier"):
        try:
            df = lire_fichier_deces(f)
            df = nettoyer_deces(df)

            LOG.info(f"Nombre de ligne après nettoyage: {len(df):_}")
            parquet_path = output_dir / (f.stem.replace("-", "_") + ".parquet")
            df.to_parquet(parquet_path, index=False)

            size_in = f.stat().st_size / 1024 / 1024
            size_out = parquet_path.stat().st_size / 1024 / 1024
            LOG.info(f"{f.name}: {size_in:.1f} Mo → {parquet_path.name}: {size_out:.1f} Mo")

            if delete_original:
                os.remove(f)
                LOG.info(f"🗑️  Fichier source supprimé : {f.name}")

        except Exception as e:
            LOG.error(f"Erreur lors de la conversion de {f.name}: {e}")

    LOG.info("✅ Conversion complète terminée.")


# ---------------------------------------------------------------------
def charger_parquet_multi(base_dir: Path) -> pd.DataFrame:
    """
    Charge tous les fichiers `.parquet` d’un dossier et les fusionne en un seul DataFrame.
    """

    fichiers = sorted(base_dir.glob("*.parquet"))
    if not fichiers:
        LOG.warning(f"Aucun fichier Parquet trouvé dans {base_dir}")
        return pd.DataFrame()

    LOG.info(f"Chargement de {len(fichiers)} fichiers Parquet depuis {base_dir}...")
    dfs = [pd.read_parquet(f) for f in fichiers]
    df = pd.concat(dfs, ignore_index=True)
    LOG.info(f"✅ Données fusionnées : {len(df):,} lignes totales.")
    return df
