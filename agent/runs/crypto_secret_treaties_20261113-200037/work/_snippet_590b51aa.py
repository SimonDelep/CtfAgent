from math import gcd
from functools import reduce

# Charger la clé publique
pubkey = []
with open('pubkey.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

print(f"Nombre d'éléments: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")
print(f"Valeurs max/min: {max(pubkey)}/{min(pubkey)}")

# Essayer de trouver n via GCD de différences
# Dans MH, w_i = m * s_i mod n
# Donc w_i - w_j = m*(s_i - s_j) mod n
# Si s_i - s_j est petit, le GCD pourrait révéler n

diffs = []
for i in range(min(20, len(pubkey))):
    for j in range(i+1, min(20, len(pubkey))):
        diffs.append(abs(pubkey[i] - pubkey[j]))

print(f"\nNombre de différences: {len(diffs)}")
print(f"Plus petites différences: {sorted(diffs)[:10]}")

# GCD de toutes les différences
g = reduce(gcd, diffs)
print(f"GCD de toutes les différences: {g}")

# GCD progressif
g = 0
for d in diffs[:100]:
    g = gcd(g, d)
    if g == 1:
        break
print(f"GCD progressif (100 premières diffs): {g}")