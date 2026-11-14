# Charger et analyser les données
with open('files/pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]
print(f"Nombre d'éléments de clé publique: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")
print(f"Valeurs max/min: {max(pubkey)} / {min(pubkey)}")
print(f"Bits max: {max(pubkey).bit_length()}")

with open('files/ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Ciphertexts: {ciphertexts}")