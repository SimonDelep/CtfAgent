import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
b64_strings = b64_pattern.findall(data.decode('latin-1'))

# Décode chaque chaîne et voir le résultat
decoded_parts = []
for i, s in enumerate(b64_strings):
    try:
        # Ajouter padding si nécessaire
        padded = s + '=' * (4 - len(s) % 4) if len(s) % 4 else s
        decoded = base64.b64decode(padded)
        decoded_parts.append(decoded)
        # Afficher les premières chaînes
        if i < 10:
            print(f"{i}: {s} -> {decoded!r}")
    except Exception as e:
        print(f"{i}: {s} -> Erreur: {e}")

# Concaténer tout
full_decoded = b''.join(decoded_parts)
print(f"\nLongueur totale décodée: {len(full_decoded)} octets")
print(f"Fin du flux: {full_decoded[-50:]!r}")