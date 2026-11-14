import numpy as np
from fpylll import IntegerMatrix, LLL, BKZ

# Vérifier l'API BKZ
print(dir(BKZ))

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

# Le problème est que les valeurs sont trop grandes pour int64.
# Une approche est d'utiliser une construction où on normalise les valeurs.

# Autre idée: au lieu d'utiliser les valeurs brutes de pubkey, on peut
# utiliser une construction où on embed le ciphertext avec un facteur de pondération
# et on cherche un vecteur court.

# Construction alternative: utiliser une matrice de taille (n+1) x (n+1)
# où les valeurs sont normalisées.

# Mais d'abord, vérifions si on peut utiliser fpylll avec des grands entiers.
# IntegerMatrix.from_matrix devrait gérer les grands entiers via Python.

# Le problème est que mat.astype(np.int64) tronque les valeurs.
# Essayons de créer la matrice directement avec des entiers Python.

# Création de matrice avec des entiers Python
def create_matrix_int(pubkey, ciphertext):
    n = len(pubkey)
    
    # Matrice de taille (n+1) x (n+1)
    # On utilise une liste de listes d'entiers Python
    mat_list = []
    for i in range(n):
        row = [0] * (n+1)
        row[i] = 1
        row[n] = pubkey[i]  # Grande valeur
        mat_list.append(row)
    
    # Dernière ligne
    last_row = [0] * n + [-ciphertext]
    mat_list.append(last_row)
    
    return mat_list

mat_list = create_matrix_int(pubkey, ct)
print(f"Taille de la matrice: {len(mat_list)} x {len(mat_list[0])}")
print(f"Valeur en [n][n]: {mat_list[n][n]}")

# Convertir en IntegerMatrix
try:
    imat = IntegerMatrix.from_list(mat_list)
    print("Conversion réussie!")
    print(f"Valeur en [n][n]: {imat[n][n]}")
except Exception as e:
    print(f"Erreur: {e}")
