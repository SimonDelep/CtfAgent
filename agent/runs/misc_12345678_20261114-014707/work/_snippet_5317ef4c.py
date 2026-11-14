import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
b64_strings = b64_pattern.findall(data.decode('latin-1'))

# Décode chaque chaîne
decoded_parts = []
for s in b64_strings:
    try:
        padded = s + '=' * (4 - len(s) % 4) if len(s) % 4 else s
        decoded = base64.b64decode(padded)
        decoded_parts.append(decoded)
    except:
        pass

full_decoded = b''.join(decoded_parts)

# Chercher 'csaw{' dans le flux décodé
print("Recherche de 'csaw{' dans le flux décodé:")
if b'csaw{' in full_decoded:
    idx = full_decoded.find(b'csaw{')
    print(f"Trouvé à la position {idx}: {full_decoded[idx:idx+50]!r}")
else:
    print("Pas trouvé directement")

# Chercher 'csaw' en hex
print("\nRecherche de 'csaw' en hex (63 73 61 77):")
if b'csaw' in full_decoded:
    idx = full_decoded.find(b'csaw')
    print(f"Trouvé à la position {idx}: {full_decoded[idx:idx+50]!r}")
else:
    print("Pas trouvé")

# Afficher tout le flux décodé en hex pour voir
print(f"\nFlux décodé complet (hex):")
print(full_decoded.hex())