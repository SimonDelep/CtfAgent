# Approche: LLL optimisé avec des entiers (pas de flottants)
# Utilisation de l'algorithme LLL avec arithmétique entière

import math

def lll_integer(matrix, delta=3, threshold=3):
    """
    LLL avec arithmétique entière pour éviter les problèmes de précision.
    delta = 3 correspond à delta=0.75 en version flottante (3/4).
    """
    n = len(matrix)
    if n == 0:
        return matrix
    
    # Copie de la matrice
    B = [row[:] for row in matrix]
    
    # Gram-Schmidt en entiers (on garde les numérateurs et dénominateurs)
    # Pour simplifier, on utilise une version simplifiée
    
    def dot(u, v):
        return sum(a * b for a, b in zip(u, v))
    
    def norm_sq(v):
        return dot(v, v)
    
    # Gram-Schmidt avec fractions
    def gram_schmidt(B):
        n = len(B)
        if n == 0:
            return [], []
        
        # B* = vecteurs orthogonaux
        B_star = [[0] * len(B[0]) for _ in range(n)]
        mu = [[0] * n for _ in range(n)]
        
        for i in range(n):
            B_star[i] = B[i][:]
            for j in range(i):
                # mu[i][j] = <B[i], B*[j]> / <B*[j], B*[j]>
                num = dot(B[i], B_star[j])
                den = norm_sq(B_star[j])
                if den != 0:
                    mu[i][j] = num / den
                    for k in range(len(B[i])):
                        B_star[i][k] -= mu[i][j] * B_star[j][k]
        
        return B_star, mu
    
    # Initialisation
    B_star, mu = gram_schmidt(B)
    
    k = 1
    max_iter = n * n * 10
    iter_count = 0
    
    while k < n and iter_count < max_iter:
        iter_count += 1
        
        # Trouver le premier j >= k-1 avec ||B*_j|| > 0
        j = k - 1
        while j < n - 1 and norm_sq(B_star[j]) == 0:
            j += 1
        
        if j >= n - 1:
            k += 1
            continue
        
        # Condition de Lovasz: ||B*_k||^2 >= (delta - mu[k][k-1]^2) * ||B*_{k-1}||^2
        # En version entière: delta * ||B*_{k-1}||^2 <= ||B*_k||^2 + mu[k][k-1]^2 * ||B*_{k-1}||^2
        # Mais on a des flottants pour mu...
        
        # Simplification: utiliser la condition standard
        norm_k_minus_1 = norm_sq(B_star[k-1])
        norm_k = norm_sq(B_star[k])
        
        if norm_k + mu[k][k-1]**2 * norm_k_minus_1 >= (delta / 4) * norm_k_minus_1:
            # Réduction de taille
            for i in range(k-1, -1, -1):
                r = round(mu[k][i])
                if abs(r) >= threshold:
                    for x in range(len(B[k])):
                        B[k][x] -= r * B[i][x]
                    B_star, mu = gram_schmidt(B)
            k += 1
        else:
            # Échange
            B[k], B[k-1] = B[k-1], B[k]
            B_star, mu = gram_schmidt(B)
            k = max(k - 1, 1)
    
    return B

# Test avec un petit exemple
test_matrix = [
    [1, 0, 100],
    [0, 1, 200],
    [0, 0, 300]
]
result = lll_integer(test_matrix)
print("LLL test:", result)

# Maintenant, appliquons au problème subset-sum
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

print(f"\nClé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")

# Pour le premier ciphertext, construisons la matrice
ct = ciphertexts[0]
n = len(pubkey)

# Matrice (n+1) x (n+1):
# [ I_n | pubkey ]
# [ 0   | ciphertext ]
# On cherche un vecteur (x_0, ..., x_{n-1}, -1) qui est court

# En fait, on veut que la dernière composante soit -ciphertext
# Donc on construit:
# [ I_n | pubkey ]
# [ 0   | 2*ciphertext ]  (pour que le vecteur solution ait -ciphertext comme dernière composante)

# Ou plus simplement:
# [ I_n | pubkey ]
# [ 0   | ciphertext ]
# Et on cherche un vecteur avec dernière composante = -ciphertext

# Construction de la matrice
size = n + 1
matrix = [[0] * size for _ in range(size)]

for i in range(n):
    matrix[i][i] = 1
    matrix[i][n] = pubkey[i]

matrix[n][n] = ciphertexts[0]

print(f"Taille de la matrice: {size}x{size}")
print("Premières lignes de la matrice:")
for i in range(min(3, size)):
    print(matrix[i][:10], "...", matrix[i][-1])

# Appliquer LLL
print("\nApplication de LLL...")
reduced = lll_integer(matrix)
print("Réduction terminée")

# Chercher un vecteur binaire
for i, row in enumerate(reduced):
    binary_part = row[:n]
    if all(x == 0 or x == 1 for x in binary_part):
        total = sum(pubkey[j] for j in range(n) if binary_part[j] == 1)
        if total == ciphertexts[0]:
            print(f"Solution trouvée à la ligne {i}!")
            print(f"Bits à 1: {sum(binary_part)}")
            break
else:
    print("Aucune solution binaire trouvée directement")
    # Afficher les premières lignes réduites
    print("\nPremières lignes réduites:")
    for i in range(min(5, len(reduced))):
        row = reduced[i]
        print(f"Ligne {i}: somme={sum(row[:n])}, derniers éléments={row[-3:]}")