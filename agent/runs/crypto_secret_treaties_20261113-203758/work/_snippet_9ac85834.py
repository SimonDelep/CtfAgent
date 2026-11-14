import numpy as np
from fpylll import IntegerMatrix, LLL, BKZ

# Lire les données
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

# Approche différente : matrice de réseau standard pour subset-sum
# On cherche x binaire tel que sum(pubkey * x) = ct
# Construction : [I_n | 0; pubkey^T | -ct]
# Mais on normalise pour éviter les overflow

# Trouver le maximum des valeurs
max_val = max(max(pubkey), ct)
print(f"max_val = {max_val}")

# Utiliser une constante C proportionnelle
# C devrait être environ sqrt(n) * max_val pour équilibrer
C = int(max_val ** 0.5) * 10
print(f"C = {C}")

# Construire la matrice
mat = []
for i in range(n):
    row = [0] * (n + 1)
    row[i] = 1
    row[n] = pubkey[i]
    mat.append(row)

# Dernière ligne
last_row = [p for p in pubkey] + [-ct]
mat.append(last_row)

print(f"Matrice taille: {len(mat)} x {len(mat[0])}")

# Convertir en IntegerMatrix
try:
    imat = IntegerMatrix.from_matrix(mat)
    print("Conversion réussie")
    
    # LLL reduction
    LLL.reduction(imat)
    print("LLL terminé")
    
    # Chercher un vecteur solution
    found = False
    for i in range(n + 1):
        row = list(imat[i])
        # Vérifier si c'est un vecteur binaire avec dernière composante = -1
        if row[-1] == -1:
            vec = row[:-1]
            if all(v in [0, 1] for v in vec):
                print(f"Solution trouvée à la ligne {i}")
                print(f"Vecteur: {vec[:20]}...")
                print(f"Poids de Hamming: {sum(vec)}")
                # Vérifier la somme
                calc_sum = sum(pubkey[j] * vec[j] for j in range(n))
                print(f"Somme calculée: {calc_sum}")
                print(f"Ciphertext: {ct}")
                if calc_sum == ct:
                    print("VALIDATION OK!")
                    found = True
                    break
        # Vérifier aussi si dernière composante est 1 (parfois le signe peut être inversé)
        elif row[-1] == 1:
            vec = row[:-1]
            if all(v in [0, 1] for v in vec):
                print(f"Vecteur binaire trouvé (dernière composante = {row[-1]})")
                print(f"Vecteur: {vec[:20]}...")
                print(f"Poids de Hamming: {sum(vec)}")
                found = True
                break
    
    if not found:
        # Afficher quelques vecteurs courts
        print("\nVecteurs courts trouvés:")
        for i in range(min(5, n + 1)):
            row = list(imat[i])
            weight = sum(1 for v in row[:-1] if v != 0)
            print(f"  Ligne {i}: dernière={row[-1]}, poids={weight}, premieres={row[:10]}")
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()