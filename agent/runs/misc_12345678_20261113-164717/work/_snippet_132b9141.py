import base64

# Les chaînes Base64 trouvées précédemment dans le fichier WAV
# On va relire le fichier et extraire toutes les chaînes Base64 potentielles

with open("12345678 (1).wav", "rb") as f:
    data = f.read()

# Chercher des motifs Base64 (caractères A-Za-z0-9+/=)
import re

# Extraire toutes les séquences de caractères Base64 d'au moins 8 caractères
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{8,}={0,2}')
matches = base64_pattern.findall(data)

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")
for i, m in enumerate(matches[:20]):
    try:
        decoded = base64.b64decode(m)
        print(f"{i}: {m} -> {decoded}")
    except:
        print(f"{i}: {m} -> (échec)")