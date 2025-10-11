import pandas as pd
from pathlib import Path


def load_csv(file_name: str) -> pd.DataFrame:
    """Charge un CSV depuis le dossier assets/data"""
    base = Path(__file__).resolve().parents[1] / "dashboard" / "assets" / "data"
    file_path = base / file_name
    return pd.read_csv(file_path)


def load_txt(file_name: str, subfolder: str = None) -> pd.DataFrame:
    """Charge un fichier texte brut (data.gouv)"""
    base = Path(__file__).resolve().parents[1] / "dashboard" / "assets" / "data"
    if subfolder:
        base = base / subfolder
    file_path = base / file_name
    return pd.read_fwf(file_path, encoding="utf-8", errors="ignore")
