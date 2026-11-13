from math import sqrt

# Lire les données
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

n = len(pubkey)
print(f"n = {n}")

# Pour chaque ciphertext, on veut résoudre subset-sum
# On va utiliser LLL via fpylll ou une implémentation simple

# D'abord, vérifions si on a fpylll
try:
    from fpylll import IntegerMatrix, LLL
    print("fpylll disponible")
except ImportError:
    print("fpylll non disponible, on va essayer une implémentation simple")