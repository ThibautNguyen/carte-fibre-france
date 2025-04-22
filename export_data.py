import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Connexion à la base de données
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

# Chargement des données fibre
query = "SELECT * FROM reseau.techno_internet_com_2024_clean"
fibre_df = pd.read_sql(query, conn)

# Fermeture de la connexion
conn.close()

# Création du dossier data s'il n'existe pas
os.makedirs('data', exist_ok=True)

# Sauvegarde en CSV
fibre_df.to_csv('data/fibre_data.csv', index=False)
print(f"Données exportées : {len(fibre_df)} communes") 