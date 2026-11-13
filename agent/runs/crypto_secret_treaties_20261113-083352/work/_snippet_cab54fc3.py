# Lisons les fichiers et analysons la structure
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

print(f"Nombre d'éléments de la clé publique: {len(pubkey)}")
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Clé publique (premiers 5): {pubkey[:5]}")
print(f"Clé publique (derniers 5): {pubkey[-5:]}")
print(f"Ciphertexts: {ciphertexts}")

# Vérifions la densité du problème
# Densité = n / log2(max(pubkey))
import math
n = len(pubkey)
max_pub = max(pubkey)
density = n / math.log2(max_pub)
print(f"Densité: {density}")

# Pour Merkle-Hellman, si la densité est faible (< 0.94), LLL peut résoudre directement
# Sinon, il faut trouver la trapdoor