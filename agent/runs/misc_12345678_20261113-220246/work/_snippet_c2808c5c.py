import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{4,}={0,2}')
matches = base64_pattern.findall(data)

# Filtrer les chaînes valides
valid_matches = []
for m in matches:
    if 4 <= len(m) <= 200:
        valid_matches.append(m)

print(f"Nombre total de chaînes: {len(valid_matches)}")

# Afficher toutes les chaînes avec leur décodage
print("\nToutes les chaînes Base64:")
for i, m in enumerate(valid_matches):
    try:
        # Ajouter padding
        padding = 4 - len(m) % 4
        if padding != 4:
            padded = m + b'=' * padding
        else:
            padded = m
        decoded = base64.b64decode(padded)
        # Afficher la chaîne et son décodage
        m_str = m.decode('ascii')
        print(f"#{i}: {m_str} -> {decoded[:30]}")
    except Exception as e:
        print(f"#{i}: {m} -> Erreur: {e}")