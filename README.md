# Carte de la couverture fibre en France métropolitaine

Application web interactive développée avec Streamlit permettant de visualiser le taux de couverture fibre optique dans les communes françaises.

## Fonctionnalités

- 🗺️ Carte interactive de la France métropolitaine
- 📊 Visualisation du taux de couverture fibre par commune
- 🎨 Code couleur intuitif (du jaune clair au vert foncé)
- 📈 Statistiques nationales (moyenne, communes 100% fibrées, communes < 50%)
- 🔍 Tooltips détaillés au survol des communes

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/carte_fibre.git
cd carte_fibre
```

2. Créer un environnement virtuel Python :
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Créer un fichier `.env` à la racine du projet :
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=opendata
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
```

## Utilisation

Lancer l'application :
```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## Structure des données

L'application utilise deux sources de données :
- Contours géographiques des communes (GeoJSON via API ADEME)
- Données de couverture fibre (Base PostgreSQL, schéma `reseau`, table `techno_internet_com_2024_clean`)

## Technologies utilisées

- Python 3.11+
- Streamlit
- Pydeck
- GeoPandas
- PostgreSQL
- psycopg2

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 