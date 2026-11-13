import requests

base_url = "http://juggler.chal.csaw.io:80"

# D'abord, on s'inscrit
s = requests.Session()

# Obtenir la page de registration pour avoir le CSRF token
r = s.get(f"{base_url}/register.php")
print("Register page status:", r.status_code)

# Extraire le CSRF token
import re
match = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
if match:
    csrf_token = match.group(1)
    print("CSRF token:", csrf_token)
else:
    print("No CSRF token found")
    csrf_token = None

# Inscription
data = {
    "username": "testuser",
    "password": "testpass123",
    "csrf_token": csrf_token if csrf_token else ""
}
r = s.post(f"{base_url}/register.php", data=data)
print("Register response:", r.status_code)
print("Redirect location:", r.headers.get("Location", "N/A"))
