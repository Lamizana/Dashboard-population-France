# Dashboard populatioçn francaise

Mise en place d'un Dashboard étudiant l'évolution de la population francaise

---

## Introduction

Ce projet a pour but d'analyser les vrais chiffres de la population (données publique 'data.gouv.fr') et d'étudier les différentes corrélation sur la violence exercées sur les femmes en france.

Le but de ce projet est de trouver des patterns sur la condition de l'agresseur et de l'agressé pour mieux prévenir le danger.

---

## Setup et installation

### Recupèrer le dépot

```bash
# Cloner le projet
git clone https://github.com/Lamizana/Dashboard-population-France
cd Dashboard-population-France
```

### Activer l'environnement virtuel

```bash
# Créer et activer un environnement virtuel (optionnel)
python3 -m venv .env 
source .env/bin/activate  # ou .venv\Scripts\activate sous Windows

# Pour verifier quel environement on utilise :
which python
/home/lamizana/projects/Dashboard-population-France/.env/bin/python
```

### Installer les librairies

```bash
pip install -r requirements.txt
```

### Gèler les dépendances dans requirements.txt si tu en rajoutes

```bash
pip freeze > requirements.txt
```

### Exécuter proprement ton script comme un module

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

<details> <summary><strong> Architecture</strong></summary>

```css
Dashboard-population-France/
│
├── dashboard/
│   ├── app.py                      # Tableau de bord Streamlit principal
│   ├── __init__.py                      
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
├── data_processed/              # données lourdes Parquet
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

---

## INSEE (Institut National de la Statistique et des Études Économiques)

> 🔹 C’est **la source officielle** des données démographiques, économiques et sociales en France.

- C’est **l’organisme producteur** des données (par exemple les fichiers des décès, naissances, recensements, revenus, etc.). 
- Les données sont **certifiées**, **contrôlées** et **documentées** par des statisticiens publics.
- C’est **la référence** pour les chiffres “officiels” utilisés par le gouvernement, les chercheurs et les médias.
- Les fichiers bruts (`naissances`, `décès`, `recensements`) viennent directement de l’état civil.

**Site officiel :** [insee.fr](https://www.insee.fr)
