from fpylll import IntegerMatrix, LLL
from fpylll.tools.basis_reduction import bkz

# Charger la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Charger les ciphertexts
ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")
print(f"Premier ciphertext: {ciphertexts[0]}")

# Vérifier que c'est bien 72 éléments
assert len(pubkey) == 72, f"Attends 72, en a {len(pubkey)}"

# Pour chaque ciphertext, on veut trouver un vecteur binaire x de longueur 72
# tel que sum(pubkey[i] * x[i]) = ciphertext

# Construction de matrice pour LLL:
# On crée une matrice de taille (n+1) x (n+1) où n=72
# Les premières n colonnes ont pubkey[i] sur la diagonale
# La dernière colonne contient le ciphertext
# On cherche un vecteur court qui correspond à la solution

# Une approche: matrice avec C * I et une colonne pour le ciphertext
# Mais pour subset-sum, on utilise souvent une matrice différente

# Approche standard: construire une matrice où on cherche un vecteur (x, -1)
# tel que sum(pubkey[i]*x[i]) - ciphertext = 0

# Matrice de taille (n+1) x (n+1):
# [ 2*pubkey[0]  0          ...  0         ciphertext ]
# [ 0           2*pubkey[1] ...  0         ciphertext ]
# [ ...                                          ...   ]
# [ 0           0          ...  2*pubkey[n-1] ciphertext ]
# [ 1           1          ...  1          0          ]

# Non, c'est plus simple: on veut trouver x binaire tel que pubkey . x = ciphertext
# On construit une matrice avec les pubkey en lignes et on cherche un vecteur court

# Approche: matrice (n+1) x (n+1)
# Ligne i (0..n-1): 2*pubkey[i] à la position i, 0 ailleurs, ciphertext à la fin
# Dernière ligne: 1 partout, 0 à la fin

# En fait, l'approche standard pour subset-sum est:
# Créer une matrice de taille (n+1) x (n+1):
# - Les n premières lignes ont 2*pubkey[i] sur la diagonale et ciphertext dans la dernière colonne
# - La dernière ligne a 1 partout et 0 dans la dernière colonne
# Après réduction LLL, on devrait trouver un vecteur avec des 0 et 1

# Mais il faut aussi pénaliser les solutions qui ne sont pas binaires
# On peut utiliser une approche avec pondération

# Essayons une approche simple d'abord
n = 72
C = 1  # facteur de pondération

# Matrice pour LLL: on cherche x tel que pubkey . x = ciphertext
# Construction: (n+1) x (n+1)
# Pour chaque i: ligne i a 2*pubkey[i] à la position i, 0 ailleurs, et ciphertext à la fin
# Dernière ligne: 1 partout, 0 à la fin

# En fait, pour subset-sum, on utilise souvent:
# Matrice de taille (n+1) x (n+1):
# [ 1  0  0 ... 0  pubkey[0] ]
# [ 0  1  0 ... 0  pubkey[1] ]
# [ ...                      ]
# [ 0  0  0 ... 1  pubkey[n-1] ]
# [ 0  0  0 ... 0  ciphertext ]
# Non, ce n'est pas ça non plus.

# L'approche correcte pour subset-sum avec LLL:
# On veut trouver x binaire tel que sum(a_i * x_i) = s
# On construit une matrice de taille (n+1) x (n+1):
# Les n premières lignes: e_i (vecteur de base) avec a_i dans la dernière colonne
# Dernière ligne: (1, 1, ..., 1, s)
# Après réduction, on cherche un vecteur avec des coefficients 0 ou 1

# En fait, la construction standard est:
# Matrice M de taille (n+1) x (n+1):
# M[i][i] = 1 pour i < n
# M[i][n] = a_i pour i < n
# M[n][j] = 1 pour j < n
# M[n][n] = s
# On cherche un vecteur v tel que v . M soit court

# Non, c'est l'inverse. On veut que M . x soit court.
# La construction correcte est:
# M = [[2*a_0, 0, ..., 0, s],
#      [0, 2*a_1, ..., 0, s],
#      ...
#      [0, 0, ..., 2*a_{n-1}, s],
#      [1, 1, ..., 1, 0]]
# Après réduction LLL, on devrait trouver un vecteur avec des 0 et 1

# Essayons cette construction
def solve_subsetsum_lll(pubkey, ciphertext):
    n = len(pubkey)
    # Matrice de taille (n+1) x (n+1)
    size = n + 1
    
    # Créer la matrice
    mat = IntegerMatrix(size, size)
    
    # Remplir la matrice
    for i in range(n):
        mat[i][i] = 2 * pubkey[i]
        mat[i][n] = ciphertext
    
    for j in range(n):
        mat[n][j] = 1
    mat[n][n] = 0
    
    # Réduire avec LLL
    LLL.reduction(mat)
    
    # Chercher un vecteur avec des 0 et 1
    for i in range(size):
        row = [mat[i][j] for j in range(size)]
        # Vérifier si c'est une solution binaire
        if all(x in [0, 1, -1] for x in row[:-1]):  # Ignorer la dernière colonne
            # Vérifier si c'est une solution valide
            x = row[:-1]
            total = sum(pubkey[j] * x[j] for j in range(n))
            if total == ciphertext:
                return x
    
    return None

# Tester sur le premier ciphertext
result = solve_subsetsum_lll(pubkey, ciphertexts[0])
if result:
    print("Solution trouvée!")
    print(f"Vecteur: {result[:10]}...")
    # Convertir en octets
    bits = result
    # 72 bits = 9 octets, MSB-first
    message = []
    for i in range(0, 72, 8):
        byte_val = 0
        for j in range(8):
            byte_val = byte_val * 2 + bits[i + j]
        message.append(byte_val)
    print(f"Message: {message}")
    print(f"ASCII: {''.join(chr(b) if 32 <= b < 127 else '?' for b in message)}")
else:
    print("Aucune solution trouvée avec cette approche")
