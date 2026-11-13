from fpylll import IntegerMatrix, LLL
import numpy as np

# Lire la clé publique
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(l) for l in lines]

# Lire le ciphertext
with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertext = [int(l) for l in lines]

n = len(pubkey)
print(f"n = {n}")

# Pour Merkle-Hellman, on peut utiliser LLL pour trouver la trapdoor
# La matrice typique est:
# [ I_n | b ]
# [ 0   | M ]
# où on cherche un vecteur court qui correspond à la séquence super-increasing

# Mais une approche plus directe est d'utiliser LLL pour résoudre le subset-sum
# Pour chaque ciphertext, on cherche un vecteur binaire x tel que sum(x[i] * pubkey[i]) = ciphertext

# Construisons une matrice pour LLL
# La matrice est de la forme:
# [ 2*pubkey[0]  2*pubkey[1]  ...  2*pubkey[n-1]  ciphertext ]
# [      0           0        ...       0          M         ]
# où M est un grand nombre

# Pour chaque ciphertext, on essaie de trouver le vecteur binaire correspondant

def solve_subset_sum_lll(pubkey, ct, M=10**40):
    n = len(pubkey)
    
    # Construire la matrice
    # On utilise une matrice de taille (n+1) x (n+1)
    # La dernière colonne contient le ciphertext
    # Les autres colonnes contiennent 2*pubkey[i]
    
    mat = IntegerMatrix(n + 1, n + 1)
    
    for i in range(n):
        mat[i, i] = 2
        mat[i, n] = pubkey[i]
    
    mat[n, n] = M
    
    # LLL reduction
    LLL.reduction(mat)
    
    # Le vecteur court devrait correspondre à la solution
    # On cherche un vecteur avec des entrées 0 ou 1 dans les premières n positions
    
    for row in range(n + 1):
        vec = [mat[row, i] for i in range(n)]
        # Vérifier si c'est un vecteur binaire
        if all(v in [0, 1, -1] for v in vec):
            # Convertir en binaire (prendre la valeur absolue)
            bits = [abs(v) for v in vec]
            # Vérifier si la somme correspond au ciphertext
            total = sum(bits[i] * pubkey[i] for i in range(n))
            if total == ct:
                return bits
    
    return None

# Essayer pour le premier ciphertext
print(f"Premier ciphertext: {ciphertext[0]}")
result = solve_subset_sum_lll(pubkey, ciphertext[0])
if result:
    print(f"Solution trouvée: {result[:20]}...")
else:
    print("Aucune solution trouvée avec M=10^40")

# Essayer avec différentes valeurs de M
for M_exp in [30, 35, 40, 45, 50]:
    M = 10**M_exp
    result = solve_subset_sum_lll(pubkey, ciphertext[0], M)
    if result:
        print(f"Solution trouvée avec M=10^{M_exp}: {result[:20]}...")
        break
else:
    print("Aucune solution trouvée avec M entre 10^30 et 10^50")