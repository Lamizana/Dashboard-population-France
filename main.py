import sys
from utils.logger import Logger

LOG = Logger()

# ---------------------------------------------------------------- #
def main() -> int:
    # TODO: Generer le dasboard Streamlit

    try:
        LOG.info("Bienvenue")

    except Exception as e:
        print("FERMETURE FORCE -")

    print("Fin de l’exécution.")
    return 0


#####################################################################
if __name__ == "__main__":
    sys.exit(main())
