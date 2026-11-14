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

# Construction CVP : on veut trouver le vecteur le plus proche de ct dans le réseau généré par pubkey
# Matrice : [I_n | 0; pubkey^T | -ct]
# Mais on utilise une approche différente : embed ct comme cible

# Alternative : utiliser BKZ avec un paramètre de bloc plus grand
# Ou essayer une construction où on multiplie par une constante pour forcer la solution

# Approche : matrice augmentée avec une colonne pour ct
# [I_n  0]
# [pubkey^T  -ct]
# Multiplié par une grande constante C pour la dernière colonne

# Trouver une constante C appropriée
# C devrait être environ n * max(pubkey) pour que la dernière colonne domine
max_pubkey = max(pubkey)
C = n * max_pubkey
print(f"C = {C}")

# Construire la matrice
mat = []
for i in range(n):
    row = [0] * (n + 1)
    row[i] = 1
    row[n] = pubkey[i] * C
    mat.append(row)

# Dernière ligne : [pubkey * C, -ct * C]
last_row = [p * C for p in pubkey] + [-ct * C]
mat.append(last_row)

print(f"Matrice taille: {len(mat)} x {len(mat[0])}")

# Convertir en IntegerMatrix
try:
    imat = IntegerMatrix.from_matrix(mat)
    print("Conversion réussie")
    
    # BKZ avec un paramètre de bloc plus grand
    # BKZ peut mieux trouver les vecteurs courts
    try:
        param = BKZ.Param(block_size=20, flags=BKZ.AUTO_PROFILING)
        BKZ.reduction(imat, param)
        print("BKZ terminé")
    except Exception as e:
        print(f"BKZ échoué, essayons LLL: {e}")
        LLL.reduction(imat)
        print("LLL terminé")
    
    # Chercher un vecteur solution
    found = False
    for i in range(n + 1):
        row = list(imat[i])
        # Vérifier si c'est un vecteur binaire avec dernière composante = -C ou -ct*C
        last = row[-1]
        vec = row[:-1]
        
        # La solution devrait avoir vec binaire et last = -ct*C (ou proche)
        # Mais après réduction, last pourrait être différent
        
        # Vérifier si vec est binaire
        if all(v in [0, 1] for v in vec):
            weight = sum(vec)
            print(f"Vecteur binaire trouvé: poids={weight}, dernière={last}")
            # Vérifier la somme
            calc_sum = sum(pubkey[j] * vec[j] for j in range(n))
            print(f"  Somme calculée: {calc_sum}")
            print(f"  Ciphertext: {ct}")
            if calc_sum == ct:
                print("  VALIDATION OK!")
                found = True
                break
    
    if not found:
        # Afficher quelques vecteurs
        print("\nPremiers vecteurs réduits:")
        for i in range(min(10, n + 1)):
            row = list(imat[i])
            vec = row[:-1]
            last = row[-1]
            weight = sum(1 for v in vec if v != 0)
            print(f"  Ligne {i}: dernière={last}, poids={weight}, vec={vec[:10]}...")
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()