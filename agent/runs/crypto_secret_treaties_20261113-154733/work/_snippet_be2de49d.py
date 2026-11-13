# Analysons la clé publique
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

# Vérifions si la séquence est super-increasing
def is_super_increasing(seq):
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

print(f"Est super-increasing: {is_super_increasing(pubkey)}")

# Vérifions les ratios entre éléments consécutifs
print("\nRatios entre éléments consécutifs:")
for i in range(min(10, len(pubkey)-1)):
    ratio = pubkey[i+1] / pubkey[i]
    print(f"  pubkey[{i+1}]/pubkey[{i}] = {ratio:.4f}")

# Vérifions la densité du problème
# Densité = n / log2(max(pubkey))
import math
n = len(pubkey)
max_val = max(pubkey)
density = n / math.log2(max_val)
print(f"\nDensité du problème: {density:.4f}")
print(f"n = {n}, log2(max) = {math.log2(max_val):.2f}")