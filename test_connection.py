import urllib.request
import socket

def test_internet_connection():
    print("Test de la connexion internet...")
    try:
        # Test avec Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Connexion internet OK (Test DNS Google)")
    except OSError as e:
        print(f"❌ Erreur de connexion internet : {e}")
        return False

    # Test des différentes URLs
    urls_to_test = [
        "https://www.google.com",
        "https://wxs.ign.fr",
        "https://cadastre.data.gouv.fr"
    ]

    for url in urls_to_test:
        print(f"\nTest d'accès à {url}")
        try:
            response = urllib.request.urlopen(url, timeout=5)
            print(f"✅ Accès OK - Status: {response.status}")
        except Exception as e:
            print(f"❌ Erreur d'accès : {e}")

    return True

if __name__ == "__main__":
    test_internet_connection() 