# Lisons la clé publique
with open('pubkey.txt', 'r') as f:
    lines = f.readlines()

pubkey = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        pubkey.append(int(line))

# Lisons les ciphertexts
with open('ciphertext.txt', 'r') as f:
    lines = f.readlines()

ciphertexts = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        ciphertexts.append(int(line))

# Affichons le premier ciphertext et la clé publique en format entier
print(f"pubkey[0] = {pubkey[0]}")
print(f"ciphertext[0] = {ciphertexts[0]}")
print(f"Nombre d'éléments: {len(pubkey)}")