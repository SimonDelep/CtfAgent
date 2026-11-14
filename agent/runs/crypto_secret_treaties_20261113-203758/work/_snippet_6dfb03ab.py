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

print(f"n = {n}")
print(f"ct = {ct}")
print(f"max(pubkey) = {max(pubkey)}")
print(f"min(pubkey) = {min(pubkey)}")

# Construction de matrice pour CVP
# On veut trouver x binaire tel que sum(pubkey * x) = ct
# Matrice: [I | 0; pubkey^T | -ct]
# Après réduction, on cherche un vecteur avec dernière composante = -1

# Utiliser une constante C pour pondérer la dernière colonne
C = 10**40  # Très grande constante

# Créer la matrice
# Taille (n+1) x (n+1)
# Les n premières lignes: identité avec pubkey dans la dernière colonne
# Dernière ligne: pubkey^T avec -ct*C

mat = []
for i in range(n):
    row = [0] * (n + 1)
    row[i] = 1
    row[n] = pubkey[i] * C
    mat.append(row)

# Dernière ligne
last_row = [p * C for p in pubkey] + [-ct * C]
mat.append(last_row)

print(f"Matrice taille: {len(mat)} x {len(mat[0])}")
print(f"Valeurs max dans matrice: {max(max(row) for row in mat)}")

# Convertir en IntegerMatrix
try:
    imat = IntegerMatrix.from_matrix(mat)
    print("Conversion réussie")
    
    # LLL reduction
    LLL.reduction(imat)
    print("LLL terminé")
    
    # Chercher un vecteur solution
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
                break
        # Vérifier aussi si dernière composante est proche de -1
        elif abs(row[-1]) <= 1:
            vec = row[:-1]
            # Vérifier si c'est binaire
            if all(v in [0, 1] for v in vec):
                print(f"Vecteur binaire trouvé (dernière composante = {row[-1]})")
                print(f"Vecteur: {vec[:20]}...")
                print(f"Poids de Hamming: {sum(vec)}")
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()