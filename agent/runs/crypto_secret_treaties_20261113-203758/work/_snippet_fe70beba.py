import numpy as np
from fpylll import IntegerMatrix, LLL, BKZ
from fpylll.tools.bkz_stats import short_vector

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

# Construction de matrice pour CVP
# On veut trouver x binaire tel que sum(x_i * pubkey_i) = ciphertext
# On construit une matrice où le vecteur solution est court

# Approche: matrice de dimension (n+1) x (n+1)
# Les n premières colonnes: base du réseau
# Dernière colonne: embedding du ciphertext

# Construction classique pour subset-sum:
# Matrice M de taille (n+1) x (n+1)
# M[i][i] = 1 pour i < n
# M[n][i] = pubkey[i] pour i < n
# M[n][n] = -ciphertext (ou une constante)

# Mais pour trouver le vecteur binaire, on peut utiliser:
# M = [[2*pubkey[0], 2*pubkey[1], ..., 2*pubkey[n-1], ciphertext],
#      [1, 0, ..., 0, 0],
#      [0, 1, ..., 0, 0],
#      ...
#      [0, 0, ..., 1, 0]]

# Ou une construction plus standard pour CVP:
# On cherche un vecteur (x_1, ..., x_n, y) tel que sum(x_i * pubkey_i) + y*c = 0
# où c est une constante grande

# Essayons la construction suivante:
# Matrice de taille (n+1) x (n+1)
# Ligne i (0 <= i < n): a des 1 sur la diagonale, et pubkey[i] dans la dernière colonne
# Dernière ligne: des 0 sauf -1 dans la dernière colonne

# En fait, pour subset-sum, la construction standard est:
# Créer une matrice où on cherche un vecteur court qui correspond à la solution binaire

# Construction: matrice de taille (n+1) x (n+1)
# Pour chaque i < n: ligne i a 1 en position i, et 0 ailleurs (sauf peut-être dernière colonne)
# Dernière ligne: pubkey[0], pubkey[1], ..., pubkey[n-1], -ciphertext

# Le vecteur solution serait (x_0, x_1, ..., x_{n-1}, 1) où x_i est binaire
# et sum(x_i * pubkey_i) = ciphertext

# Mais cela ne force pas x_i à être binaire. On doit ajouter une contrainte.

# Une construction meilleure: utiliser une matrice où les x_i sont "pénalisés" s'ils ne sont pas 0 ou 1
# Ou utiliser BKZ avec une taille de bloc plus grande

# Essayons d'abord une construction simple et voyons ce que LLL trouve

def solve_subsetsum_lll(pubkey, ciphertext, c_factor=1):
    n = len(pubkey)
    
    # Construction de matrice pour CVP
    # On veut trouver x tel que sum(x_i * pubkey_i) = ciphertext
    # Matrice de taille (n+1) x (n+1)
    
    # Création de la matrice
    mat = np.zeros((n+1, n+1), dtype=np.int64)
    
    # Les n premières lignes: identité
    for i in range(n):
        mat[i][i] = 1
    
    # Dernière ligne: pubkey et -ciphertext
    for i in range(n):
        mat[n][i] = pubkey[i]
    mat[n][n] = -ciphertext
    
    # Convertir en IntegerMatrix pour fpylll
    # Mais les valeurs peuvent être trop grandes pour int64...
    # On doit utiliser une approche différente
    
    return mat

# Test avec le premier ciphertext
ct = ciphertexts[0]
print(f"Traitement du premier ciphertext: {ct}")

# La construction ci-dessus peut avoir des problèmes avec les grandes valeurs
# Essayons une construction avec échelle

# Construction alternative: 
# On normalise les valeurs pour qu'elles tiennent dans int64
# Ou on utilise une construction différente

# Pour subset-sum, une construction courante est:
# Matrice de taille (n+1) x (n+1)
# M[i][j] = delta_{i,j} pour i < n, j < n (identité)
# M[i][n] = 0 pour i < n
# M[n][j] = pubkey[j] pour j < n
# M[n][n] = -ciphertext

# Le vecteur (x_0, ..., x_{n-1}, 1) a pour image (x_0, ..., x_{n-1}, sum(x_i*pubkey_i) - ciphertext)
# Si sum(x_i*pubkey_i) = ciphertext, alors le vecteur image est (x_0, ..., x_{n-1}, 0)

# Mais on cherche un vecteur court dans le réseau, pas son image.

# Construction correcte pour CVP:
# On veut trouver x binaire tel que sum(x_i * pubkey_i) = ciphertext
# On construit un réseau généré par les colonnes de:
# [I_n | 0]
# [pubkey^T | -ciphertext]

# Et on cherche un vecteur court qui est une combinaison linéaire entière des colonnes.

# En fait, la construction standard pour subset-sum est différente:
# On crée une matrice où chaque colonne i (pour i < n) a:
# - 1 en position i
# - pubkey[i] en position n
# Et la dernière colonne a:
# - 0 partout sauf -ciphertext en position n

# Le vecteur solution est (x_0, x_1, ..., x_{n-1}, 1) où x_i est binaire.

# Essayons cette construction:

def solve_subsetsum_v2(pubkey, ciphertext):
    n = len(pubkey)
    
    # Matrice de taille (n+1) x (n+1)
    # Colonne i (i < n): 1 en position i, pubkey[i] en position n
    # Colonne n: 0 partout sauf -ciphertext en position n
    
    mat = np.zeros((n+1, n+1), dtype=object)  # Utiliser object pour grandes valeurs
    
    for i in range(n):
        mat[i][i] = 1
        mat[n][i] = pubkey[i]
    
    mat[n][n] = -ciphertext
    
    return mat

mat = solve_subsetsum_v2(pubkey, ct)
print("Matrice construite (premières lignes):")
print(mat[:5, :5])
print(f"Valeur en [n][n]: {mat[n][n]}")
