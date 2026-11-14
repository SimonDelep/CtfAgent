import numpy as np
from math import log2

# Charger les données
pubkey = []
with open('pubkey.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

ciphertexts = []
with open('ciphertext.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")

# Vérifier la densité
max_w = max(pubkey)
bits = 72
density = bits / log2(max_w)
print(f"Densité: {density:.4f} (bits={bits}, log2(max_w)={log2(max_w):.2f})")

# Pour LLL, on construit une matrice de dimension (n+1) x (n+1)
# La matrice est:
# [ I_n   0  ]
# [ w^T  c ]
# où w est le vecteur de la clé publique et c est le ciphertext
# On cherche un vecteur court qui correspond au message binaire

# Mais une meilleure construction pour subset-sum est:
# [ I_n    0  ]
# [ 2*w^T  2*c ]
# ou utiliser une constante C pour pondérer

# Essayons avec une matrice où on cherche x tel que w.x = c
# La matrice est:
# [ I_n      0 ]
# [ w^T    -c ]
# et on cherche un vecteur (x, 1) ou (x, -1)

# Construction alternative: matrice de dimension (n+1)
# L = [ I_n    0  ]
#     [ w^T   -c ]
# Après réduction LLL, on devrait trouver un vecteur de la forme (x, 1) où x est binaire

# Testons sur le premier ciphertext
n = len(pubkey)
c = ciphertexts[0]

# Construire la matrice
# On utilise une approche où on pondère fortement la dernière colonne
C = 2  # facteur de pondération

# Matrice de taille (n+1) x (n+1)
# Les premières n lignes ont un 1 sur la diagonale
# La dernière ligne a w_i * C et -c * C

mat = np.zeros((n+1, n+1), dtype=object)
for i in range(n):
    mat[i, i] = 1
mat[n, :n] = [w * C for w in pubkey]
mat[n, n] = -c * C

print(f"\nMatrice de taille {mat.shape}")
print(f"Valeurs dans la dernière ligne (premiers 5): {mat[n, :5]}")
print(f"Valeur en (n,n): {mat[n,n]}")

# Sauvegarder pour LLL
np.savetxt('/tmp/mh_mat.txt', mat, fmt='%s')
print("Matrice sauvegardée")