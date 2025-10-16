#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de conversion massive des fichiers décès INSEE
TXT → Parquet optimisé.

À exécuter depuis la racine du projet :
    python main_convert.py
"""

from pathlib import Path
from utils.data_loader import convert_to_parquet
from utils.logger import Logger

LOG = Logger("convert_main.log")


#####################################################################
def main():

    try:
        # Dossiers d’entrée et de sortie
        source_dir = Path("data_processed/deces")
        output_dir = Path("data_processed/deces")

        LOG.info("🚀 Démarrage de la conversion massive INSEE (TXT → Parquet)")

        convert_to_parquet(
            source_dir=source_dir,
            output_dir=output_dir,
            delete_original=True,  # ⚠️ Mets True si tu veux supprimer les .txt après conversion
        )

    except Exception as e:
        LOG.error(f"FERMETURE FORCE - {e}")
        return 1
    else:
        LOG.info("✅ Conversion terminée avec succès.")
        LOG.info(f"Fichiers Parquet disponibles dans : {output_dir.resolve()}")
    finally:
        LOG.separator()

    return 0


#####################################################################
if __name__ == "__main__":
    main()
