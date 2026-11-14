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

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")
print(f"Premier ciphertext: {ciphertexts[0]}")

# Tester la méthode lagarias sur le premier ciphertext
from fpylll import IntegerMatrix, LLL, BKZ
import numpy as np

def solve_lagarias(pubkey, ciphertext):
    n = len(pubkey)
    c = n + 1
    
    # Matrice de taille (n+1) x (n+1)
    mat = np.zeros((n+1, n+1), dtype=np.float64)
    
    for i in range(n):
        mat[i][i] = 1.0
        mat[i][n] = float(c * pubkey[i])
    
    mat[n][n] = float(c * ciphertext)
    
    # Convertir en IntegerMatrix
    try:
        imat = IntegerMatrix.from_matrix(mat.astype(np.int64))
    except Exception as e:
        print(f"Erreur conversion: {e}")
        return None
    
    # LLL reduction
    LLL.reduction(imat)
    
    # Chercher un vecteur avec composantes 0/1 et dernière composante -1
    for i in range(n+1):
        vec = np.array(imat[i])
        # Vérifier si c'est un vecteur binaire (sauf dernière composante)
        if vec[-1] == -1:
            if np.all((vec[:-1] == 0) | (vec[:-1] == 1)):
                # Vérifier la somme
                if np.sum(vec[:-1].astype(int) * pubkey) == ciphertext:
                    return vec[:-1].astype(int)
    
    return None

result = solve_lagarias(pubkey, ciphertexts[0])
print(f"Résultat lagarias: {result}")

# Essayer BKZ avec différentes tailles de bloc
def solve_bkz(pubkey, ciphertext, block_size=10):
    n = len(pubkey)
    
    mat = np.zeros((n+1, n+1), dtype=np.float64)
    
    for i in range(n):
        mat[i][i] = 1.0
        mat[n][i] = float(pubkey[i])
    mat[n][n] = float(-ciphertext)
    
    try:
        imat = IntegerMatrix.from_matrix(mat.astype(np.int64))
    except Exception as e:
        print(f"Erreur conversion BKZ: {e}")
        return None
    
    # BKZ reduction
    try:
        bkz = BKZ.BlockReduction(block_size=block_size)
        bkz(imat)
    except Exception as e:
        print(f"Erreur BKZ: {e}")
        return None
    
    for i in range(n+1):
        vec = np.array(imat[i])
        if np.all((vec[:-1] == 0) | (vec[:-1] == 1)):
            if np.sum(vec[:-1].astype(int) * pubkey) == ciphertext:
                return vec[:-1].astype(int)
    
    return None

for bs in [10, 15, 20, 25, 30]:
    result = solve_bkz(pubkey, ciphertexts[0], block_size=bs)
    print(f"BKZ block_size={bs}: {result}")
