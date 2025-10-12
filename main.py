import sys
from utils.data_loader import convert_to_parquet
from utils.logger import Logger

LOG = Logger("main.log")


#####################################################################
def main() -> int:

    try:
        LOG.info("Bienvenue")
    except Exception as e:
        LOG.error(f"FERMETURE FORCE - {e}")
        return 1
    finally:
        LOG.info("Fin de l’exécution.")
        LOG.separator()

    return 0


#####################################################################
if __name__ == "__main__":
    sys.exit(main())
