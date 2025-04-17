import psycopg2
from dotenv import load_dotenv
import os

def test_connection():
    # Chargement des variables d'environnement
    load_dotenv()
    
    try:
        # Tentative de connexion
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "opendata"),
            user=os.getenv("DB_USER", "cursor_ai"),
            password=os.getenv("DB_PASSWORD", "cursor_ai_is_quite_awesome")
        )
        print("✅ Connexion à la base de données réussie!")
        
        # Test de la requête
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reseau.techno_internet_com_2024_clean")
        count = cur.fetchone()[0]
        print(f"✅ Nombre d'enregistrements dans la table : {count}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur de connexion : {str(e)}")

if __name__ == "__main__":
    test_connection() 