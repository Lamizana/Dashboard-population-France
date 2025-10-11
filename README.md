# 🧠 cours_IA

Mise en place de différentes applications d’**intelligence artificielle** avec **Scikit-learn**.

---

## Introduction

Ce projet a pour but d'analyser les vrais chiffres de la population (données publique 'data.gouv.fr') et d'étudier 
les différentes corrélation sur la violence exercées sur les femmes en france.

Le but de ce projet est de trouver des patterns sur la condition de l'agresseur et de l'agressé pour mieux prévenir 
le danger.

## 📚 Sommaire

- [Setup et installation](#setup-et-installation)
- [Utilisation (déroulable)](#utilisation-déroulable)
  - [TODO avec PyCharm](#todo-avec-pycharm)
  - [Journalisation (Logging)](#journalisation-logging)

---

## ⚙️ Setup et installation

### Architecture du projet

- Les données sont **publiques** et ont ete récupérées `data.gouv.fr`.

```css
Dashboard-population-France/
│
├── dashboard/
│   ├── app.py                      # Tableau de bord principal (Streamlit)
│   ├── sections/
│   │   ├── population.py           # Recensement population
│   │   ├── naissance.py            # Statistiques naissance
│   │   ├── deces.py                # Statistiques décès
│   │   ├── viols.py                # Statistiques viols
│   │   ├── féminicides.py          # Statistiques féminicides
│   │   └── __init__.py
│   └── assets/
│       ├── cartes/                 # Images et cartes générées
│       └── data/
│           └── deces/
│               ├── deces-2025-m08.txt
│           ├── population.csv
│           └── emploi.csv
│
├── utils/
│   ├── logger.py                   # Logger coloré
│   ├── data_loader.py              # Fonctions de chargement / nettoyage de données
│   ├── plot_utils.py               # Fonctions pour graphiques (matplotlib / seaborn)
│   └── __init__.py
│
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Configuration Docker
├── docker-compose.yml              # Pour exécution et port mapping
└── main.py                         # Tests unitaires / pipeline local
```



### 🧩 Recupèrer le dépot

```bash
# Cloner le projet
git clone https://github.com/Lamizana/Dashboard-population-France
cd Dashboard-population-France
```

### 🧩 1️⃣ Activer l'environnement virtuel

```bash
# Créer et activer un environnement virtuel (optionnel)
python3 -m venv .env 
source .env/bin/activate  # ou .venv\Scripts\activate sous Windows

# Pour verifier quel environement on utilise :
which python
/home/lamizana/projects/Dashboard-population-France/.env/bin/python
```

### 🧩 2️⃣ Installer les librairies

```bash
pip install -r requirements.txt
```

### 🧩 3️⃣ Gèler les dépendances dans requirements.txt si tu en rajoutes

```bash
pip freeze > requirements.txt
```

### 🧩 4️⃣ Exécuter proprement ton script comme un module

Depuis la racine de du projet (Dashboard-population-France/), exécuter :

```python
python3 main.py
```

```python
python3 -m sections.deces
```

---

## Utilisations

<details> <summary><strong>🧩 Cliquer pour dérouler la section d'utilisation</strong></summary>

### TODO avec Pycharm

#### ✅ 1. Ecrire une TODO dans le code

Il faut simplement ajouter un _comentaire spécial_ dans le code :

```python
# TODO: implémenter la fonction de nettoyage des données INSEE
def clean_data():
    pass
```

Il y a plusieurs variantes :

```python
# FIXME: corriger la normalisation PCA
# FEAT: Nouvel feature.
# HACK: solution rapide, à améliorer plus tard
```

#### 2. 🧭 Voir toutes les TODO dans Pycharm

1. Ouvrir le projet.
2. Va dans menu :
   1. **View -> Tool Windows -> TODO**
3. Une fenêtre s'ouvre avec la liste des TODO trouvé dans le code :
   1. Le fichier concerné.
   2. La ligne exacte.
   3. Le contenu en commentaire.

> 💡 Cliquer sur une ligne pour aller directement au code.

#### 3. Ajouter tes propres filtres TODO

On a défini des **règles personalisées** (par exemple `@urgent`, `@review`, etc.) :

1. Aller dans :
   1. **File → Settings → Editor → TODO**

2. Cliquer sur ➕ pour ajouter une nouvelle règle :
   1. **Pattern** : `@urgent.*`
   2. **Case sensitive** : coché ou non selon ton besoin
   3. Choisir une couleur d'affichage.

Les TODO seront ensuite colorées à la vue dédiée.

Tu verras ensuite ces TODO colorés différemment dans la vue dédiée.

### 🧾 Journalisation (Logging)

Le projet utilise un système de journalisation centralisé basé sur un module `logger.py`, 
afin d’enregistrer les messages d’exécution et les erreurs dans un fichier de log.

--- 

#### 📁 Structure du fichier

Le logger est défini dans :

```css
cours_IA/
├── logger.py
└── recensement_population/
    ├── main.py
    └── ...
```

#### ⚙ Fonctionnement

Le fichier `logger.py` contient une classe `Logger` personnalisée, qui :

- Enregistre les messages dans un fichier (ex. `recensement_pop.log`) ;
- Affiche aussi les messages dans la console pour le suivi en temps réel.

#### 🧩 Exemple d’utilisation

```python
# main.py
from logger import Logger

# Initialisation du logger (le fichier 'app.logs/' sera créé automatiquement)
log = Logger("logs/recensement_pop.log")


def main() -> int:
   log.info("Démarrage de l’application...")
   # ton code ici
   log.info("Fin de l’exécution.")
   return 0


if __name__ == "__main__":
   import sys

   sys.exit(main())
```

🧠 Exemple de sortie dans app.log

```yaml
2025-10-11 15:24:53,872 - INFO - Démarrage de l’application...
2025-10-11 15:24:55,123 - INFO - Fin de l’exécution.
```
