# 📁 Données — Fichier des décès (INSEE / data.gouv.fr)

Les données utilisées dans ce module proviennent du **fichier des personnes décédées**, mis à disposition par l’**INSEE** via la plateforme [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/).

---

## 🔍 Description du jeu de données

Le **fichier des personnes décédées** recense, pour chaque individu déclaré décédé en France depuis 1970 :

- le nom et prénom,
- la date et le lieu de naissance,
- la date et le lieu du décès,
- le sexe,
- un identifiant unique par enregistrement.

Les fichiers sont mis à jour **chaque mois** et publiés sous la forme de fichiers texte (`.txt`) à large volume, disponibles année par année.

---

## 🧩 Structure du fichier  

Le fichier est fourni au format **texte brut (.txt)**, avec des champs à **positions fixes**.  
Chaque enregistrement correspond à **une personne décédée**.  

| Champ | Longueur | Position | Type | Description |
|:------|:----------|:----------|:------|:-------------|
| **Nom et prénom** | 80 | 1–80 | Alphanumérique | Forme : `NOM*PRENOMS` |
| **Sexe** | 1 | 81 | Numérique | `1 = Masculin` ; `2 = Féminin` |
| **Date de naissance** | 8 | 82–89 | Numérique | Forme : `AAAAMMJJ` (`AAAA=0000` si année inconnue ; `MM=00` si mois inconnu ; `JJ=00` si jour inconnu) |
| **Code du lieu de naissance** | 5 | 90–94 | Alphanumérique | Code Officiel Géographique (COG) en vigueur au moment du décès |
| **Commune de naissance (en clair)** | 30 | 95–124 | Alphanumérique | Nom de la commune de naissance |
| **DOM/TOM/COM/Pays de naissance (en clair)** | 30 | 125–154 | Alphanumérique | Nom du territoire ou du pays de naissance |
| **Date de décès** | 8 | 155–162 | Numérique | Forme : `AAAAMMJJ` (même codification que la date de naissance) |
| **Code du lieu de décès** | 5 | 163–167 | Alphanumérique | Code Officiel Géographique du lieu de décès |
| **Numéro d’acte de décès** | 9 | 168–176 | Alphanumérique | Numéro d’acte — ⚠️ certains enregistrements peuvent contenir des caractères non significatifs en fin de ligne |

---

## 🧠 Remarques importantes  

- Les fichiers peuvent contenir plusieurs millions d’enregistrements.  
- Il est recommandé de les manipuler avec des outils adaptés (**Python / pandas**, **Spark**, ou des bases de données).  
- Le format à positions fixes facilite le découpage des colonnes avec `pandas.read_fwf()` ou un script personnalisé.

📎 Exemple de fichier utilisé :  
[`deces-2024.txt`](https://static.data.gouv.fr/resources/fichier-des-personnes-decedees/20250210-094840/deces-2024.txt)

> ⚠️ Le fichier est en **texte brut** avec des largeurs de champs fixes (format FWF).  
> Il doit être lu via `pandas.read_fwf()` pour être correctement interprété.

---

## 🧮 Exemple d’utilisation dans le projet

Le module `utils/data_loader.py` contient une fonction de lecture :

---

## 🗂️ Organisation locale

Les fichiers texte sont stockés dans le répertoire :

```swift
dashboard/assets/data/deces/
```

```swift
dashboard/assets/data/deces/
 └── deces-2024.txt
 └── deces-2023.txt
```

---

## ⚙️Traitement des données

Une fois le fichier chargé :

- Les dates sont converties en format **datetime**.

- Un âge au décès est calculé pour chaque enregistrement.

- Les valeurs aberrantes sont filtrées (age < 0 ou age > 140).

- Les données nettoyées peuvent être exportées en `.parquet` .

Exemples :

```python
df["date_naissance"] = pd.to_datetime(df["date_naissance"], format="%Y%m%d", errors="coerce")
df["date_deces"] = pd.to_datetime(df["date_deces"], format="%Y%m%d", errors="coerce")
df["age_deces"] = ((df["date_deces"] - df["date_naissance"]).dt.days / 365.25).round(0)
```

---

## 📊 Visualisation

Les données de décès sont exploitées dans plusieurs visualisations :

- Carte de répartition des décès par département.

- Carte de l’âge moyen au décès.

- Carte à cercles proportionnels (âge moyen).

- Histogrammes et statistiques descriptives.

Les fichiers générés sont enregistrés dans :

```bash
dashboard/assets/cartes/
```

---

## 📚 Source officielle

- **Fichier des personnes décédées — INSEE**
    > https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/

- Licence : [Licence Ouverte / Etalab 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence/)
- Producteur : **INSEE**
- Mise à jour : mensuelle
- Format : `.txt` (Fixed Width File)
