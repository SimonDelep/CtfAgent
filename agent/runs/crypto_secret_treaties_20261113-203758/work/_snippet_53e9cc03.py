import numpy as np
from fpylll import IntegerMatrix, LLL, BKZ

# Charger les données
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
ct = ciphertexts[0]

print(f"n = {n}, ct = {ct}")

# Construction de matrice pour subset-sum
# On veut trouver x binaire tel que sum(x_i * pubkey_i) = ciphertext

# Construction standard: matrice de taille (n+1) x (n+1)
# Colonne i (i < n): 1 en position i, pubkey[i] en position n
# Colonne n: 0 partout sauf -ciphertext en position n

# Le vecteur solution est (x_0, x_1, ..., x_{n-1}, 1) où x_i est binaire.
# La norme de ce vecteur est sqrt(sum(x_i^2) + 1) = sqrt(poids + 1)

# Mais le problème est que les valeurs pubkey[i] sont très grandes, donc
# le vecteur (x_0, ..., x_{n-1}, 1) n'est pas nécessairement le plus court.

# On doit ajouter une pondération pour forcer la dernière composante à être petite.

# Construction avec pondération:
# Matrice M de taille (n+1) x (n+1)
# M[i][i] = 1 pour i < n
# M[n][i] = pubkey[i] * w pour i < n (w est un facteur de pondération)
# M[n][n] = -ciphertext * w

# Ou on peut utiliser une construction différente où on embed le ciphertext
# dans une colonne séparée avec un facteur de pondération.

# Essayons la construction suivante:
# On crée une matrice où on cherche un vecteur (x_0, ..., x_{n-1}, y) tel que
# sum(x_i * pubkey_i) + y * C = 0 où C est une constante grande.
# Si y = -1, alors sum(x_i * pubkey_i) = C.

# Mais on veut sum(x_i * pubkey_i) = ciphertext, pas C.

# Construction correcte pour CVP (Closest Vector Problem):
# On veut trouver x tel que sum(x_i * pubkey_i) est proche de ciphertext.
# On construit un réseau généré par les colonnes de:
# [I_n | 0]
# [pubkey^T | 1]

# Et on cherche le vecteur du réseau le plus proche de (0, 0, ..., 0, ciphertext).

# En pratique, on peut utiliser la construction:
# Matrice de taille (n+1) x (n+1)
# Ligne i (i < n): 1 en position i, 0 ailleurs
# Ligne n: pubkey[0], pubkey[1], ..., pubkey[n-1], -ciphertext

# Le vecteur (x_0, ..., x_{n-1}, 1) est dans le réseau si sum(x_i * pubkey_i) = ciphertext.

# Mais pour que ce vecteur soit court, on doit s'assurer que les autres vecteurs du réseau
# sont plus longs.

# Une construction courante est d'utiliser une matrice de la forme:
# [2*pubkey[0], 2*pubkey[1], ..., 2*pubkey[n-1], ciphertext]
# [1, 0, ..., 0, 0]
# [0, 1, ..., 0, 0]
# ...
# [0, 0, ..., 1, 0]

# Le vecteur solution est (x_0, x_1, ..., x_{n-1}, -1) où x_i est binaire.
# La norme est sqrt(sum(x_i^2) + 1) = sqrt(poids + 1).

# Mais les valeurs 2*pubkey[i] sont très grandes, donc ce n'est pas idéal.

# Essayons une construction avec échelle:
# On divise toutes les valeurs par un facteur commun pour les rendre plus petites.

# Ou on utilise BKZ avec une taille de bloc plus grande.

# Pour l'instant, essayons la construction simple et voyons ce que LLL trouve.

# Construction: matrice de taille (n+1) x (n+1)
# M[i][j] = delta_{i,j} pour i < n, j < n
# M[i][n] = 0 pour i < n
# M[n][j] = pubkey[j] pour j < n
# M[n][n] = -ciphertext

# Convertir en IntegerMatrix
# Les valeurs peuvent être très grandes, donc on doit utiliser une représentation appropriée.

# fpylll utilise des int64, donc on doit s'assurer que les valeurs tiennent dans int64.
# Le maximum de pubkey est environ 7.9e28, ce qui est trop grand pour int64 (max ~9e18).

# On doit donc utiliser une construction où les valeurs sont plus petites, ou utiliser
# une bibliothèque qui supporte les grands entiers.

# Une alternative est d'utiliser la construction où on normalise les valeurs.

# Essayons d'abord de voir si on peut utiliser fpylll avec des valeurs réduites.

# On peut diviser toutes les valeurs par un facteur commun, mais cela change le problème.

# Une meilleure approche: utiliser une construction où on embed le ciphertext
# avec un facteur de pondération approprié.

# Construction de Lagarias-Odlyzko pour subset-sum:
# Matrice de taille (n+1) x (n+1)
# M[i][j] = delta_{i,j} + (n+1) * delta_{i,n} * delta_{j,n} pour i, j < n
# M[i][n] = (n+1) * a_i pour i < n
# M[n][j] = 0 pour j < n
# M[n][n] = (n+1) * S

# où a_i sont les éléments de la clé publique et S est le ciphertext.

# Cette construction garantit que le vecteur solution est court.

# Essayons cette construction:

def solve_subsetsum_lagarias(pubkey, ciphertext):
    n = len(pubkey)
    c = n + 1  # Facteur de pondération
    
    # Matrice de taille (n+1) x (n+1)
    mat = np.zeros((n+1, n+1), dtype=object)
    
    # Lignes 0 à n-1
    for i in range(n):
        mat[i][i] = 1
        mat[i][n] = c * pubkey[i]
    
    # Dernière ligne
    for j in range(n):
        mat[n][j] = 0
    mat[n][n] = c * ciphertext
    
    return mat

mat = solve_subsetsum_lagarias(pubkey, ct)
print("Matrice construite (premières lignes):")
print(mat[:5, :5])
print(f"Valeur en [n][n]: {mat[n][n]}")

# Vérifier la taille des valeurs
max_val = max(max(row) for row in mat)
print(f"Valeur maximale dans la matrice: {max_val}")
print(f"bit_length: {max_val.bit_length()}")
