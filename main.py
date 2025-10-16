import sys
from utils.loader import lire_fichier_naissances
from utils.logger import Logger

LOG = Logger("main.log")


#####################################################################
def main() -> int:

    try:
        LOG.info("Bienvenue")
        df = lire_fichier_naissances("./data_processed/naissances/naissances_2022.parquet")
        print(df)
    except Exception as e:
        LOG.error("FERMETURE FORCE - ", {e})
        return 1
    finally:
        LOG.info("Fin de l’exécution.")
        LOG.separator()

    return 0


#####################################################################
if __name__ == "__main__":
    sys.exit(main())
