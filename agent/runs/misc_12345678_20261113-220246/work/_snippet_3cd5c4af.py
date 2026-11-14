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

print("Toutes les chaînes Base64 trouvées:")
for i, m in enumerate(valid_matches):
    try:
        decoded = base64.b64decode(m)
        # Vérifier si c'est du texte ASCII lisible
        try:
            text = decoded.decode('ascii')
            if text.isprintable() or 'csaw' in text.lower():
                print(f"#{i}: {m} -> '{text}'")
        except:
            pass
    except:
        pass

# Chercher spécifiquement 'csaw' ou 'flag' dans le fichier brut
print("\n--- Recherche de 'csaw' dans le fichier brut ---")
idx = data.find(b'csaw')
if idx >= 0:
    print(f"Trouvé à la position {idx}: {data[idx:idx+20]}")
else:
    print("Pas trouvé directement")

# Chercher aussi en Base64
print("\n--- Recherche de 'Y3Nhdw==' (csaw en Base64) ---")
idx = data.find(b'Y3Nhdw==')
if idx >= 0:
    print(f"Trouvé à la position {idx}: {data[idx:idx+30]}")
else:
    print("Pas trouvé")