# Lire la clé publique et les ciphertexts
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

print(f"Nombre d'éléments de la clé publique: {len(pubkey)}")
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Max pubkey: {max(pubkey)}")
print(f"Min pubkey: {min(pubkey)}")
print(f"Log2(max pubkey): {max(pubkey).bit_length()}")

# Vérifier la densité
n = len(pubkey)
log_max = max(pubkey).bit_length()
density = n / log_max
print(f"Densité: {density}")

# Afficher les premiers éléments
print(f"Premiers 5 éléments de pubkey: {pubkey[:5]}")
print(f"Premiers 3 ciphertexts: {ciphertexts[:3]}")