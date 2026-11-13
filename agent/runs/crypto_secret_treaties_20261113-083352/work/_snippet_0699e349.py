# Charger la clé publique
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]
print(f"Nombre d'éléments: {len(pubkey)}")
print(f"Max: {max(pubkey)}")
print(f"Min: {min(pubkey)}")
print(f"Sum: {sum(pubkey)}")

# Charger les ciphertexts
with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")