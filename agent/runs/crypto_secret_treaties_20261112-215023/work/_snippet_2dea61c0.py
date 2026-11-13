# Lisons la clé publique et comptons les éléments
with open('pubkey.txt', 'r') as f:
    lines = f.readlines()

# Filtrer les lignes qui sont des nombres
pubkey = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        pubkey.append(int(line))

print(f"Nombre d'éléments dans la clé publique: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")
print(f"Derniers éléments: {pubkey[-5:]}")

# Lisons les ciphertexts
with open('ciphertext.txt', 'r') as f:
    lines = f.readlines()

ciphertexts = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        ciphertexts.append(int(line))

print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Ciphertexts: {ciphertexts}")

# Vérifions la taille des nombres
print(f"\nTaille en bits du plus grand élément de la clé publique: {max(pubkey).bit_length()}")
print(f"Taille en bits du premier ciphertext: {ciphertexts[0].bit_length()}")