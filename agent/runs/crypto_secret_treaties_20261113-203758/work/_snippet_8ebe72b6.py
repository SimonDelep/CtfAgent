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

# Essayons de créer une IntegerMatrix directement
# IntegerMatrix peut être créé avec des dimensions et on peut assigner les valeurs

imat = IntegerMatrix(n+1, n+1)

# Remplir la matrice
for i in range(n):
    imat[i, i] = 1
    imat[i, n] = pubkey[i]

for j in range(n):
    imat[n, j] = 0
imat[n, n] = -ct

print(f"Matrice créée. Valeur en [n][n]: {imat[n, n]}")

# LLL reduction
try:
    LLL.reduction(imat)
    print("LLL réduction réussie!")
    
    # Chercher un vecteur court
    for i in range(n+1):
        vec = [imat[i, j] for j in range(n+1)]
        # Vérifier si c'est un vecteur binaire (sauf dernière composante)
        if vec[-1] == -1:
            if all(v == 0 or v == 1 for v in vec[:-1]):
                # Vérifier la somme
                if sum(vec[j] * pubkey[j] for j in range(n)) == ct:
                    print(f"Solution trouvée à la ligne {i}: {vec[:-1]}")
                    print(f"Vérification: sum = {sum(vec[j] * pubkey[j] for j in range(n))}")
                    break
        elif vec[-1] == 1:
            # Peut-être que le vecteur a 1 en dernière position
            if all(v == 0 or v == 1 for v in vec[:-1]):
                if sum(vec[j] * pubkey[j] for j in range(n)) == ct:
                    print(f"Solution trouvée à la ligne {i}: {vec[:-1]}")
                    break
    
    # Afficher quelques vecteurs réduits
    print("\nPremiers vecteurs réduits:")
    for i in range(min(5, n+1)):
        vec = [imat[i, j] for j in range(n+1)]
        print(f"Ligne {i}: poids={sum(1 for v in vec if v != 0)}, dernier={vec[-1]}")
        
except Exception as e:
    print(f"Erreur LLL: {e}")
    import traceback
    traceback.print_exc()
