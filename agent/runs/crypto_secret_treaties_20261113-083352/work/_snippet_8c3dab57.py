# Lisons la clé publique et les ciphertexts
pubkey = []
with open('files/pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

ciphertexts = []
with open('files/ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Nombre d'éléments pubkey: {len(pubkey)}")
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")
print(f"Clé publique (premiers 10): {pubkey[:10]}")