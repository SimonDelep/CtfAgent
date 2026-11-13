# Vérifions d'abord la structure des données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]
print(f"Nombre d'éléments de la clé publique: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")