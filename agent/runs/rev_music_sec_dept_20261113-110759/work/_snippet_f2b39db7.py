with open('session.bin', 'rb') as f:
    data = f.read()

# Trouver la position de "flag{"
flag_start = data.find(b'flag{')
print(f"Position de 'flag{{': {flag_start}")

# Trouver où commence la clé s4lt26
key_pos = data.find(b's4lt26')
print(f"Position de 's4lt26': {key_pos}")

# Extraire les données entre flag{ et s4lt26
encrypted = data[flag_start+5:key_pos]
print(f"Longueur des données chiffrées: {len(encrypted)}")
print(f"Données chiffrées (hex): {encrypted[:50].hex()}")

# La clé est "s4lt26"
key = b's4lt26'

# Essayer XOR avec la clé
decrypted = []
for i, b in enumerate(encrypted):
    decrypted.append(b ^ key[i % len(key)])

print(f"Décrypté: {bytes(decrypted)}")