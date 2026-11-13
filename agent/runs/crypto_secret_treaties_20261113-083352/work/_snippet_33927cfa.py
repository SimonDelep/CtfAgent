# Écrivons un script pour chercher la trapdoor
# Dans Merkle-Hellman, on a:
# - Une séquence super-croissante S (private key)
# - w et m tels que gcd(w, m) = 1
# - n = w * m + 1 (ou n est un module > sum(S))
# - pubkey[i] = (S[i] * w) mod n

# Pour inverser: on cherche w, m tels que:
# S[i] = (pubkey[i] * w_inv) mod n forme une séquence super-croissante

# Une approche: tester différentes valeurs de m, calculer w = m^{-1} mod n
# puis vérifier si la séquence résultante est super-croissante

import math

def is_superincreasing(seq):
    """Vérifie si une séquence est super-croissante"""
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

# Trouver n - dans MH, n est généralement > sum(super)
# Et pubkey[i] = (super[i] * w) mod n
# Donc n doit être > max(pubkey)

n = sum(pubkey) + 1  # Hypothèse: n = sum + 1
print(f"n = {n}")

# Pour trouver w, on teste différentes valeurs de m
# w = m^{-1} mod n, et on vérifie si (pubkey[i] * w) mod n est super-croissant

def find_trapdoor(pubkey, n, max_m=1000000):
    for m in range(2, max_m):
        if math.gcd(m, n) != 1:
            continue
        # Calculer w = m^{-1} mod n
        try:
            w = pow(m, -1, n)
        except:
            continue
        
        # Calculer la séquence candidate
        seq = [(p * w) % n for p in pubkey]
        
        # Vérifier si super-croissante
        if is_superincreasing(seq):
            return (w, m, seq)
    
    return None

# Essayons avec une borne plus élevée
print("Recherche de trapdoor...")
result = find_trapdoor(pubkey, n, max_m=10000000)
if result:
    w, m, seq = result
    print(f"Trouvé! w={w}, m={m}")
    print(f"Premiers éléments de la séquence super-croissante: {seq[:10]}")
else:
    print("Pas trouvé avec m < 10000000")