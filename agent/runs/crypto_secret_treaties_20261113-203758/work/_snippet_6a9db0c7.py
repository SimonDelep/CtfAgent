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

# Construction avec facteur de pondération plus grand
# On utilise c = 2^n ou une valeur très grande pour forcer la dernière composante à être -1

# Construction: matrice de taille (n+1) x (n+1)
# Ligne i (i < n): 1 en position i, c * pubkey[i] en position n
# Dernière ligne: 0 partout sauf c * ct en position n

# Le vecteur solution est (x_0, ..., x_{n-1}, -1) où x_i est binaire.
# La norme au carré est sum(x_i^2) + c^2.

# Si c est très grand, alors le vecteur solution est très long, ce qui n'est pas idéal.
# On veut que le vecteur solution soit court.

# En fait, la construction de Lagarias-Odlyzko utilise c = n+1, et le vecteur solution
# a une norme de sqrt(n/4 + (n+1)^2 * S^2) où S est le ciphertext.

# Le problème est que S est très grand, donc la norme est très grande.

# Une construction alternative est d'utiliser une matrice où on embed le ciphertext
# dans une colonne séparée avec un facteur de pondération.

# Construction: matrice de taille (n+1) x (n+1)
# Colonne i (i < n): 1 en position i, pubkey[i] en position n
# Colonne n: 0 partout sauf -ct en position n

# Le vecteur solution est (x_0, ..., x_{n-1}, 1) où x_i est binaire.
# La norme au carré est sum(x_i^2) + 1 = poids + 1.

# Mais le problème est que les autres vecteurs du réseau peuvent être plus courts.

# Essayons une construction où on ajoute une contrainte pour que les x_i soient 0 ou 1.
# On peut utiliser une matrice de la forme:
# [2*pubkey[0], 2*pubkey[1], ..., 2*pubkey[n-1], ct]
# [1, 0, ..., 0, 0]
# [0, 1, ..., 0, 0]
# ...
# [0, 0, ..., 1, 0]

# Le vecteur solution est (x_0, x_1, ..., x_{n-1}, -1) où x_i est binaire.
# La norme au carré est sum(x_i^2) + 1 = poids + 1.

# Mais les valeurs 2*pubkey[i] sont très grandes, donc ce n'est pas idéal.

# Essayons une construction différente: utiliser BKZ avec une taille de bloc plus grande.

# D'abord, créons la matrice de base
imat = IntegerMatrix(n+1, n+1)

for i in range(n):
    imat[i, i] = 1
    imat[i, n] = pubkey[i]

for j in range(n):
    imat[n, j] = 0
imat[n, n] = -ct

# Utiliser BKZ avec une taille de bloc plus grande
# BKZ.Param est utilisé pour configurer BKZ
try:
    param = BKZ.Param(block_size=40, flags=BKZ.DEFAULT)
    bkz = BKZ.Reduction(param)
    bkz(imat)
    print("BKZ réduction réussie!")
    
    # Chercher un vecteur solution
    found = False
    for i in range(n+1):
        vec = [imat[i, j] for j in range(n+1)]
        if vec[-1] == -1 or vec[-1] == 1:
            if all(v == 0 or v == 1 for v in vec[:-1]):
                if sum(vec[j] * pubkey[j] for j in range(n)) == ct:
                    print(f"Solution trouvée à la ligne {i}: {vec[:-1]}")
                    found = True
                    break
    
    if not found:
        print("Aucune solution trouvée avec BKZ block_size=40")
        # Afficher les vecteurs réduits
        print("\nPremiers vecteurs réduits:")
        for i in range(min(10, n+1)):
            vec = [imat[i, j] for j in range(n+1)]
            print(f"Ligne {i}: poids={sum(1 for v in vec if v != 0)}, dernier={vec[-1]}")
            
except Exception as e:
    print(f"Erreur BKZ: {e}")
    import traceback
    traceback.print_exc()
