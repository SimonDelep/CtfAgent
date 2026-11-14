import numpy as np

# Charger les données
with open('pubkey.txt', 'r') as f:
    pubkey = [int(x) for x in f.read().strip().split()]

with open('ciphertext.txt', 'r') as f:
    ciphertexts = [int(x) for x in f.read().strip().split()]

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")
print(f"Premier ciphertext: {ciphertexts[0]}")
print(f"Max pubkey: {max(pubkey)}")
print(f"Min pubkey: {min(pubkey)}")

# Vérifier la densité
n = len(pubkey)
density = n / np.log2(max(pubkey))
print(f"Densité: {density:.3f}")