import requests

# Essayons localhost
base_url = "http://localhost:80"

cookies = {"PHPSESSID": "ce47992e92992aef3f61c87e3241d85c"}

# Essayons de récupérer le profil
try:
    resp = requests.get(f"{base_url}/profile.php", cookies=cookies, timeout=5)
    print("Status:", resp.status_code)
    print("Response:", resp.text[:1500])
except Exception as e:
    print("Error:", e)