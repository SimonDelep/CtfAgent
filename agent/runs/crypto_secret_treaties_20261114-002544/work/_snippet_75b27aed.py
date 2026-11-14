import numpy as np

# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

n = len(pubkey)
target = ciphertexts[0]

# Construction pour CVP:
# On veut trouver x binaire tel que pubkey.x = target
# Lattice: [ I_n    0  ]
#          [ pubkey  target ]
# La solution est (x_1, ..., x_n, -1) où x_i est binaire
# Et la dernière coordonnée du vecteur lattice est -target + sum(pubkey*x) = 0

# En fait, pour SVP on embed la cible:
# [ I_n    0  ]
# [ 2*pubkey  -2*target ]
# Chercher un vecteur avec dernière coordonnée = -1

# Ou construction alternative:
# [ I_n    0  ]
# [ pubkey  target ]
# et chercher un vecteur avec dernière coordonnée = 1

# Essayons: matrice (n+1) x (n+1)
# Ligne i (i < n): e_i + pubkey[i] * e_n
# Ligne n: target * e_n

# Non, la construction correcte est:
# b_i = e_i pour i = 0..n-1 (vecteurs de base standards)
# b_n = (pubkey_0, pubkey_1, ..., pubkey_{n-1}, target)
# On cherche combinaison linéaire entière avec dernière coordonnée = 1

# En fait, on veut:
# sum(c_i * b_i) = (x_0, x_1, ..., x_{n-1}, sum(c_i * pubkey[i]) + c_n * target)
# Pour que la dernière coordonnée soit 1, on veut c_n = 1 et sum(c_i * pubkey[i]) + target = 1
# Donc sum(c_i * pubkey[i]) = 1 - target

# Hmm, c'est compliqué. Essayons une construction plus simple:
# [ I_n    0  ]
# [ pubkey  target ]
# Si on prend combinaison avec c_n = -1, on obtient:
# (c_0, ..., c_{n-1}, sum(c_i * pubkey[i]) - target)
# Pour que ce soit court, on veut sum(c_i * pubkey[i]) ≈ target

from fpylll import IntegerMatrix, LLL

# Construction: 
# Les n premières lignes sont les vecteurs de base avec pubkey dans la dernière colonne
# La dernière ligne est (0, 0, ..., 0, target)
M = IntegerMatrix(n + 1, n + 1)

for i in range(n):
    M[i, i] = 1
    M[i, n] = pubkey[i]

M[n, n] = target

print("Matrice avant LLL:")
print(f"Dernière ligne: {[M[n, j] for j in range(n+1)]}")

# LLL reduction
LLL.reduction(M)

print("\nAprès LLL:")
# Chercher un vecteur avec dernière coordonnée = 1 ou -1
for i in range(n + 1):
    row = [M[i, j] for j in range(n + 1)]
    if abs(row[-1]) == 1:
        print(f"Vecteur {i}: last={row[-1]}")
        print(f"Premiers éléments: {row[:10]}")
        # Vérifier si c'est une solution binaire
        bits = row[:n]
        if all(b in [0, 1] for b in bits):
            total = sum(pubkey[j] * bits[j] for j in range(n))
            print(f"Solution binaire trouvée! Somme = {total}, target = {target}")
            print(f"Bits: {bits}")
        else:
            print(f"Bits non-binaires: {bits[:10]}...")

# Afficher quelques vecteurs courts
print("\nVecteurs courts (last != 0):")
for i in range(n + 1):
    row = [M[i, j] for j in range(n + 1)]
    if row[-1] != 0:
        length = sum(x*x for x in row)
        print(f"Vecteur {i}: last={row[-1]}, len={length}, premiers={row[:5]}")