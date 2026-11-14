import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles (caractères A-Za-z0-9+/=)
# On cherche des séquences d'au moins 4 caractères valides Base64
base64_chars = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')

# Trouver toutes les séquences continues de caractères Base64
resultats = []
i = 0
while i < len(data):
    if data[i:i+1] in base64_chars:
        start = i
        while i < len(data) and data[i:i+1] in base64_chars:
            i += 1
        seq = data[start:i]
        if len(seq) >= 4:  # Minimum pour Base64
            resultats.append((start, seq))
    else:
        i += 1

print(f"Nombre de séquences Base64 trouvées: {len(resultats)}")

# Afficher les premières et dernières séquences
for idx, (pos, seq) in enumerate(resultats[:10]):
    print(f"{idx}: pos={pos}, len={len(seq)}, seq={seq}")

print("...")
for idx, (pos, seq) in enumerate(resultats[-10:], len(resultats)-10):
    print(f"{idx}: pos={pos}, len={len(seq)}, seq={seq}")