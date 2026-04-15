# Données — Fichier des naissances (INSEE / data.gouv.fr)

> Pour le détail complet des variables et la documentation officielle INSEE :
[Consulter le PDF complet (naissance.pdf)](../naissances)
---

## Naissances 2024

Le fichier "Naissances" contient **14 variables** et **660 787 observations**.

Le fichier détail des naissances 2024 porte sur **l’ensemble des naissances vivantes ayant eu lieu en France (France métropolitaine et 5 DOM)** , quel que soit le lieu de domicile de la mère.

---

### Description du jeu de données

| **Code**     | **Définition**                                                                 | **Modalités** |
|---------------|--------------------------------------------------------------------------------|----------------|
| `AGEMERE`     | Âge de la mère ayant accouché à la naissance de l’enfant (en âge atteint dans l’année) | 17 : 17 ans ou moins<br>18–45 : de 18 à 45 ans<br>46 : 46 ans ou plus |
| `AGEXACTM`    | Âge exact de la mère ayant accouché à la naissance de l’enfant (en années révolues) | 17 : 17 ans ou moins<br>18–45 : de 18 à 45 ans<br>46 : 46 ans ou plus |
| `ANAIS`       | Année de naissance de l’enfant                                                | 2024 : fichier des naissances 2024 |
| `DEPDOMM`     | Département de domicile de la mère ayant accouché                             | 01–976 : départements français<br>99 : COM ou étranger |
| `DEPNAIS`     | Département de naissance de l’enfant                                           | 01–976 : départements français |
| `GAGEXAPOM`   | Groupe d’âge du second parent (en âge en années révolues)                     | 10 : 12–17 ans<br>15 : 18–19 ans<br>20 : 20–24 ans<br>25 : 25–29 ans<br>30 : 30–34 ans<br>35 : 35–39 ans<br>40 : 40–44 ans<br>45 : 45–49 ans<br>50 : 50–54 ans<br>55 : 55–59 ans<br>60 : 60–64 ans<br>65 : 65 ans ou plus |
| `GAGPOM`      | Groupe d’âge du second parent (en âge atteint dans l’année)                   | 10 : 12–17 ans<br>15 : 18–19 ans<br>20 : 20–24 ans<br>25 : 25–29 ans<br>30 : 30–34 ans<br>35 : 35–39 ans<br>40 : 40–44 ans<br>45 : 45–49 ans<br>50 : 50–54 ans<br>55 : 55–59 ans<br>60 : 60–64 ans<br>65 : 65 ans ou plus |
| `INDLNM`      | Indicateur du lieu de naissance de la mère ayant accouché                     | 1 : Née en France métropolitaine<br>2 : Née dans un DOM<br>3 : Née dans un COM<br>4 : Née à l’étranger |
| `INDNATM`     | Indicateur de nationalité de la mère ayant accouché                           | 1 : Française<br>2 : Étrangère |
| `MNAIS`       | Mois de naissance de l’enfant                                                 | 01–12 : janvier à décembre |
| `NBENF`       | Nombre d’enfants issus de l’accouchement                                      | 1 : 1 enfant<br>2 : 2 enfants<br>3 : 3 enfants ou plus |
| `REGDOMM`     | Région de domicile de la mère ayant accouché                                  | 01 : Guadeloupe<br>02 : Martinique<br>03 : Guyane<br>04 : La Réunion<br>06 : Mayotte<br>11 : Île-de-France<br>24 : Centre – Val de Loire<br>27 : Bourgogne – Franche-Comté<br>28 : Normandie<br>32 : Hauts-de-France<br>44 : Grand Est<br>52 : Pays de la Loire<br>53 : Bretagne<br>75 : Nouvelle-Aquitaine<br>76 : Languedoc-Roussillon – Midi-Pyrénées<br>84 : Auvergne – Rhône-Alpes<br>93 : Provence-Alpes-Côte d’Azur<br>94 : Corse<br>99 : COM ou étranger |
| `REGNAIS`     | Région de naissance de l’enfant                                               | mêmes codes que `REGDOMM` |
| `SEXE`        | Sexe de l’enfant                                                              | 1 : Masculin<br>2 : Féminin |

---

## Remarques importantes  

## Exemple d’utilisation dans le projet

Le module `utils/data_loader.py` contient une fonction de lecture :

---

## Organisation locale

```swift
dashboard/assets/data/naissances/
```

```swift
dashboard/assets/data/deces/
 └── deces-2024.txt
 └── deces-2023.txt
```

---

## Source officielle 

- **Fichier des naissances — INSEE**
    > https://www.insee.fr/fr/recherche?q=naissances&debut=0

- Licence : [Licence Ouverte / Etalab 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence/)
- Producteur : **INSEE**
- Mise à jour : mensuelle
- Format : `.txt` (Fixed Width File)
