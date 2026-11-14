import numpy as np

# Charger la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

print(f"Nombre d'éléments de clé publique: {len(pubkey)}")

# Charger les ciphertexts
ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Nombre de blocs de ciphertext: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")

# Vérifier que la clé publique n'est pas super-croissante
def is_superincreasing(arr):
    total = 0
    for x in arr:
        if x <= total:
            return False
        total += x
    return True

print(f"Clé publique super-croissante? {is_superincreasing(pubkey)}")

# Vérifier la densité: n / log2(max(pubkey))
n = len(pubkey)
max_val = max(pubkey)
log_max = max_val.bit_length()
density = n / log_max
print(f"Densité: {density:.4f} (n={n}, log2(max)={log_max})")
