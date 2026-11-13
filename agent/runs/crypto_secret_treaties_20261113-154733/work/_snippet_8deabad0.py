# Lire la clé publique
pubkey = []
with open('files/pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

print(f"Nombre d'éléments de la clé publique: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")
print(f"Valeurs max: {max(pubkey)}")
print(f"log2(max): {max(pubkey).bit_length()}")

# Lire les ciphertexts
ciphertexts = []
with open('files/ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"\nNombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")