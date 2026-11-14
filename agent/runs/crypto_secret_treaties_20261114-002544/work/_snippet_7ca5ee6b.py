import numpy as np

# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

n = len(pubkey)

# Tester avec fpylll
try:
    from fpylll import IntegerMatrix, LLL, BKZ
    
    # Créer une matrice
    M = IntegerMatrix(n + 1, n + 1)
    
    # Remplir la matrice
    for i in range(n):
        M[i, i] = 1
        M[i, n] = pubkey[i]
    
    M[n, n] = ciphertexts[0]
    
    print(f"Matrice créée: {M.dim[0]}x{M.dim[1]}")
    print(f"Première ligne: {[M[0, j] for j in range(5)]}...")
    print(f"Dernière ligne: {[M[n, j] for j in range(5)]}...")
    
    # LLL reduction
    LLL.reduction(M)
    
    print("LLL réduction terminée")
    
    # Vérifier les vecteurs réduits
    for i in range(n + 1):
        row = [M[i, j] for j in range(n + 1)]
        if row[-1] != 0:
            print(f"Vecteur {i}: last={row[-1]}, premiers éléments={row[:5]}")
            
except Exception as e:
    import traceback
    traceback.print_exc()