import base64

# Le flux décodé complet
full_decoded = bytes.fromhex('4481455805447e6b179039bb6ab65fe5beab6ab667e5fea7fa3fe7ce48cf9cf9139079f5af4ad09dd3bd3bebee83139039d5eda1d80b4174d33e71e73dd58d74b7dbbd9f49f4bfdc3d9749b4c7dbfd9749b4bfdc7d9348f4c3db7d8f49b4b7db3d9749f4c3dc3d8f48f4bfdb7d9349f4c3dbbd974974cbdb3d8b4a342c849320d14e202443325f35743340315faac4c344325f35743340315f')

# Trouver la position de '2_5t3@1_'
marker = b'2_5t3@1_'
pos = full_decoded.find(marker)
print(f"Position de '2_5t3@1_': {pos}")

# Le flux avant le premier '2_5t3@1_'
before_marker = full_decoded[:pos]
print(f"Longueur avant le premier marqueur: {len(before_marker)}")
print(f"Contenu avant: {before_marker[-50:]}")

# Peut-être que le flag est XORé avec 'csaw{' comme clé
# Cherchons si 'csaw{' XORé avec quelque chose apparaît
target = b'csaw{'
# Si on XOR 'csaw{' avec la clé, on obtient le ciphertext
# Donc ciphertext XOR clé = 'csaw{'
# Ou ciphertext XOR 'csaw{' = clé

# Essayons de trouver 'csaw{' en XORant chaque octet avec différentes clés
# Peut-être que la clé est répétitive

# Une autre approche: peut-être que le flag est simplement dans les métadonnées
# et que '2_5t3@1_' est le contenu du flag

# Regardons si 'csaw{' apparaît dans le fichier original
with open('audio.wav', 'rb') as f:
    data = f.read()

if b'csaw{' in data:
    idx = data.find(b'csaw{')
    print(f"\n'csaw{' trouvé à position {idx}")
    print(f"Contexte: {data[idx:idx+50]}")
else:
    print("\n'csaw{' non trouvé dans le fichier original")

# Cherchons 'flag' ou autres mots-clés
for keyword in [b'flag', b'FLAG', b'CTF', b'ctf']:
    if keyword in data:
        idx = data.find(keyword)
        print(f"'{keyword.decode()}' trouvé à position {idx}: {data[idx:idx+30]}")