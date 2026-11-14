# Charger la clé publique et les ciphertexts
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

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Premier élément: {pubkey[0]}")
print(f"Ciphertexts: {len(ciphertexts)} blocs")
print(f"Premier ciphertext: {ciphertexts[0]}")

# Vérifier la taille des nombres
print(f"Taille en bits du premier pubkey: {pubkey[0].bit_length()}")
print(f"Taille en bits du premier ciphertext: {ciphertexts[0].bit_length()}")