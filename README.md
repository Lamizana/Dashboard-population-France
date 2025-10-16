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

```bash
python3 main.py
```

```bash
python3 -m sections.deces
```

- Lancer le Dadshboard en local :
```bash
streamlit run dashboard/app.py
```

---

## Architecture et compréhension du projet

<details> <summary><strong>🧩 Architecture</strong></summary>

```css
Dashboard-population-France/
│
├── dashboard/
│   ├── app.py                      # Tableau de bord Streamlit principal
│   ├── __init__.py                      # Tableau de bord Streamlit principal
│   ├── sections/
│   │   ├── population.py
│   │   ├── naissance.py
│   │   ├── deces.py
│   │   ├── viols.py
│   │   ├── feminicides.py
│   │   └── __init__.py
│   └── assets/
│       ├── cartes/
│       └── data/
│           ├── deces/
│           │   └── deces-2025.txt
│           ├── population.csv
│           ├── emploi.csv
│           └── naissance.csv
│
│
├── data_processed/              # ✅ données lourdes Parquet
│   └── deces/
│       ├── deces_2020.parquet
│       ├── deces_2021.parquet
│       ├── ...
├── utils/
│   ├── logger.py
│   ├── data_loader.py
│   ├── plot_utils.py
│   └── __init__.py
│
├── __init__.py
├── requirements.txt
└── main.py

```

</details>

1. Le projet est centralisé avec **Docker**.
2. L'application est dirigée par **Streamlit**.
3. Les fichiers du gouvrenement francais sur le recensement de la population sont des `.txt`
   1. Ils sont récupérés sur `data.gouv.fr`
   2. C'est public, donc gratuit, vous pouvez tous savoir.
   3. Il y a une quantité astromique de données publiques.
   4. Et elles sont **anonimisées** !

- `dashboard/app.py` — **point d’entrée Streamlit**.

### 

---

## Utilisations

<details> <summary><strong>🧩 Cliquer pour dérouler la section d'utilisation</strong></summary>

### Les pull Request (Pr)

- Toujours commencer par un ``git pull``.

```bash
> git checkout -b Prefix/name_pull_request
> git commit -am "Prefix:name_pull_request"
> git push
```

Allez sur github et créer une pull request, remplir le formulaire et les labels puis l'envoyer

### Création d'une nouvelle branche

Créer une nouvelle branche ***feature/...*** à partir de la branche principale ``develop``  et la pousser vers le dépôt Git distant, voici les étapes à suivre :

Se placer sur la branche de base et la mettre à jour :

```bash
git checkout develop
git pull origin develop
```

Créer et basculer sur la nouvelle branche :

```bash
git checkout -b feature/...
```

Pousse la nouvelle branche sur le dépôt distant :

```bash
git push -u origin feature/...
```


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
