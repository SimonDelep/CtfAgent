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

# Afficher la fin des données
print(f"\nDerniers 50 octets en hex: {full_decoded[-50:].hex()}")
print(f"Derniers 50 octets en ASCII: {full_decoded[-50:]}")

# Chercher toutes les occurrences de '2_5t3@1_'
pattern = b'2_5t3@1_'
idx = 0
count = 0
while True:
    idx = full_decoded.find(pattern, idx)
    if idx == -1:
        break
    print(f"Occurrence à la position {idx}")
    count += 1
    idx += 1

print(f"\nTotal occurrences de '2_5t3@1_': {count}")

# Peut-être que le flag est dans les chaînes Base64 elles-mêmes, pas décodées
# Cherchons 'csaw' dans les chaînes Base64 brutes
print("\n--- Recherche de 'csaw' ou 'flag' dans les chaînes Base64 brutes ---")
for i, m in enumerate(valid_matches):
    m_str = m.decode('ascii', errors='replace')
    if 'csaw' in m_str.lower() or 'flag' in m_str.lower():
        print(f"#{i}: {m}")