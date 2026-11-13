# Lire la clé publique
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(l) for l in lines]
print(f"Nombre d'éléments dans la clé publique: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")
print(f"Derniers éléments: {pubkey[-5:]}")

# Lire le ciphertext
with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertext = [int(l) for l in lines]
print(f"Nombre de blocs de ciphertext: {len(ciphertext)}")
print(f"Ciphertext: {ciphertext}")