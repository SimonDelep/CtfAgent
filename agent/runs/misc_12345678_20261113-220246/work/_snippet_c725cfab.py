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

# Fonction pour décoder avec padding correct
def safe_b64decode(s):
    # Ajouter le padding si nécessaire
    padding = 4 - len(s) % 4
    if padding != 4:
        s += b'=' * padding
    try:
        return base64.b64decode(s)
    except:
        return b''

# Décode toutes les chaînes et concaténer
full_decoded = b''.join([safe_b64decode(m) for m in valid_matches])

print(f"Longueur totale: {len(full_decoded)} octets")
print(f"En hexadécimal (premier 200 octets):")
print(full_decoded[:200].hex())

# Vérifier si c'est du texte ASCII déguisé
print(f"\nEn ASCII (remplaçant les non-imprimables par .):")
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in full_decoded))

# Chercher des patterns hexadécimaux
hex_pattern = re.compile(rb'[0-9a-fA-F]{2,}')
hex_matches = hex_pattern.findall(full_decoded)
print(f"\nNombre de séquences hexadécimales trouvées: {len(hex_matches)}")

# Essayer de convertir les séquences hex en texte
for hm in hex_matches[:10]:
    try:
        decoded_hex = bytes.fromhex(hm.decode('ascii'))
        print(f"Hex {hm} -> {decoded_hex}")
    except:
        pass