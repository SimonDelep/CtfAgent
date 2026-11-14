import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher qsTDRC spécifiquement
idx = data.find(b'qsTDRC')
print(f"Position de 'qsTDRC': {idx}")
if idx >= 0:
    # Afficher le contexte autour
    start = max(0, idx - 20)
    end = min(len(data), idx + 20)
    print(f"Contexte: {data[start:end]}")
    print(f"Hex autour: {data[start:end].hex()}")

# Maintenant, cherchons toutes les séquences de caractères Base64 avec un pattern plus flexible
# On cherche des séquences d'au moins 4 caractères qui sont valides Base64
base64_pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'

# Trouver toutes les occurrences
matches = list(re.finditer(base64_pattern, data))
print(f"\nNombre total de matches: {len(matches)}")

# Vérifier si qsTDRC est dans les matches
for m in matches:
    if b'qsTDRC' in m.group():
        print(f"Trouvé: {m.group()} à position {m.start()}")

# Afficher les matches autour de la position de qsTDRC
if idx >= 0:
    print(f"\nMatches autour de position {idx}:")
    for m in matches:
        if abs(m.start() - idx) < 100:
            print(f"  pos={m.start()}, len={len(m.group())}, match={m.group()}")