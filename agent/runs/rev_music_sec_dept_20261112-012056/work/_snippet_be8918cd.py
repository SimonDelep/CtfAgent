# Lire le fichier binaire
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher la séquence 81 66 81 6c 81 61 81 67 81 7b (flag{ avec préfixe 0x81)
flag_pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
flag_start = data.find(flag_pattern)

# Après flag{, il y a 0x81 0x0a 0x02 0x00 0x00 0x00
# Peut-être que 0x81 0x0a est un séparateur, et 0x02 0x00 0x00 0x00 est la longueur (2?)
# Ou peut-être que 0x02 0x00 0x00 0x00 indique quelque chose d'autre

# Les données chiffrées semblent commencer après ces headers
# Offset 140 semble être le début des données chiffrées réelles
encrypted_start = 140
salt_start = data.find(b's4lt26')

print("Salt position:", salt_start)
print("Longueur des données chiffrées:", salt_start - encrypted_start)

encrypted_data = data[encrypted_start:salt_start]
print("Données chiffrées (hex):", encrypted_data.hex())
print("Longueur:", len(encrypted_data))

# Essayons différentes clés
keys_to_try = [
    b'M4ch1n3_K3y!!',
    b's4lt26',
    b'v2rom',
    b'strip',
]

for key in keys_to_try:
    decrypted = bytearray()
    for i, b in enumerate(encrypted_data):
        decrypted.append(b ^ key[i % len(key)])
    print(f"\nClé: {key}")
    print(f"Décrypté: {decrypted}")
    # Vérifier si le résultat contient des caractères imprimables
    printable = sum(1 for c in decrypted if 32 <= c < 127)
    print(f"Caractères imprimables: {printable}/{len(decrypted)}")
