import requests

# Service est sur http://juggler.chal.csaw.io:80/
base_url = "http://juggler.chal.csaw.io:80"

# On a déjà un cookie PHPSESSID
cookies = {"PHPSESSID": "ce47992e92992aef3f61c87e3241d85c"}

# Essayons de récupérer le profil pour voir le token CSRF
resp = requests.get(f"{base_url}/profile.php", cookies=cookies)
print("Status:", resp.status_code)
print("Response:", resp.text[:1000])