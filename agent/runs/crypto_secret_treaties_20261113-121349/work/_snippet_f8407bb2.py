# Analyser les relations entre éléments de la clé publique
# Si b[i] = (a[i] * w) mod m et a[i] = 2^i, alors b[i+1] ≈ 2*b[i] mod m

with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(l) for l in lines]

n = len(pubkey)

# Vérifier les relations b[i+1] vs 2*b[i]
print("Analyse des relations b[i+1] vs 2*b[i]:")
for i in range(min(10, n-1)):
    b_i = pubkey[i]
    b_i1 = pubkey[i+1]
    two_bi = 2 * b_i
    
    # b[i+1] devrait être égal à (2 * b[i]) mod m
    # Donc b[i+1] = 2*b[i] ou b[i+1] = 2*b[i] - m (ou 2*b[i] - k*m)
    
    diff = two_bi - b_i1
    print(f"b[{i}] = {b_i}")
    print(f"b[{i+1}] = {b_i1}")
    print(f"2*b[{i}] = {two_bi}")
    print(f"2*b[{i}] - b[{i+1}] = {diff}")
    print()

# Si a[i] = 2^i, alors b[i] = (2^i * w) mod m
# Donc b[i] * 2 = (2^{i+1} * w) mod m = b[i+1] (mod m)
# Donc b[i] * 2 - b[i+1] = k * m pour certains k

# Regardons les différences 2*b[i] - b[i+1]
print("\nDifférences 2*b[i] - b[i+1]:")
diffs = []
for i in range(n-1):
    diff = 2 * pubkey[i] - pubkey[i+1]
    diffs.append(diff)
    if i < 10:
        print(f"2*b[{i}] - b[{i+1}] = {diff}")

# Si ces différences sont multiples de m, alors m divise leur GCD
import math
from functools import reduce

# Calculer le GCD de toutes les différences
def gcd_list(lst):
    return reduce(math.gcd, lst)

# Prendre les valeurs absolues
abs_diffs = [abs(d) for d in diffs if d != 0]
print(f"\nNombre de différences non nulles: {len(abs_diffs)}")

if len(abs_diffs) > 0:
    gcd_all = gcd_list(abs_diffs[:10])  # GCD des 10 premières
    print(f"GCD des 10 premières différences: {gcd_all}")
    
    # Essayer avec plus de différences
    if len(abs_diffs) >= 20:
        gcd_all = gcd_list(abs_diffs[:20])
        print(f"GCD des 20 premières différences: {gcd_all}")