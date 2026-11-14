import sys
sys.path.insert(0, '/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/crypto_secret_treaties_20261114-002544/forge')

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

# Importer fpylll
from fpylll import IntegerMatrix, LLL
from fpylll.util import lattice

def solve_subsetsum_lll(pubkey, target):
    """
    Résout subset-sum en utilisant LLL sur une matrice d'embedding.
    Construction: matrice (n+1)x(n+1) où les n premières lignes sont la base canonique
    et la dernière ligne contient la clé publique, avec la cible dans la dernière colonne.
    """
    n = len(pubkey)
    
    # Construction de la matrice pour CVP/SVP
    # On veut trouver un vecteur binaire x tel que sum(pubkey[i]*x[i]) = target
    # Matrice d'embedding: on ajoute une dimension pour la contrainte
    
    # Approche: matrice (n+1) x (n+1)
    # Les n premières colonnes: base identité * C (pour forcer les coefficients à être petits)
    # Dernière colonne: pubkey
    # Dernière ligne: [0,0,...,0, -target] ou similaire
    
    # Construction standard pour subset-sum:
    # Matrice M de taille (n+1) x (n+1):
    # [ C*I_n   pubkey ]
    # [ 0       -target]
    # où C est une constante grande
    
    # En fait, pour SVP on cherche un vecteur court qui correspond à la solution
    # Construction: 
    # M[i,j] = C if i==j < n
    # M[i,n] = pubkey[i] for i < n
    # M[n,j] = 0 for j < n
    # M[n,n] = -target (ou target)
    
    # Le vecteur solution serait [x_0, x_1, ..., x_{n-1}, 1] où x_i sont les bits
    # et la dernière coordonnée donne -target + sum(pubkey[i]*x[i]) = 0
    
    C = 2  # Constante de pondération - on essaie avec 2 d'abord
    
    mat = IntegerMatrix(n + 1, n + 1)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                mat[i, j] = C
            else:
                mat[i, j] = 0
        mat[i, n] = pubkey[i]
    
    for j in range(n):
        mat[n, j] = 0
    mat[n, n] = -target
    
    # Réduire avec LLL
    LLL.reduction(mat)
    
    # Vérifier les vecteurs réduits
    for i in range(n + 1):
        vec = [mat[i, j] for j in range(n + 1)]
        # Vérifier si c'est une solution potentielle
        # La dernière coordonnée devrait être +/- 1
        if abs(vec[-1]) == 1:
            # Vérifier si les premières coordonnées sont 0 ou 1 (ou -1, 0, 1)
            bits = vec[:-1]
            # Calculer la somme
            s = sum(pubkey[j] * bits[j] for j in range(n))
            if s == target:
                return bits, vec
    
    return None, None

# Tester sur le premier ciphertext
print("Résolution du premier ciphertext...")
bits, vec = solve_subsetsum_lll(pubkey, ciphertexts[0])
if bits:
    print("Solution trouvée!")
    print("Bits:", bits)
    print("Vecteur complet:", vec)
else:
    print("Pas de solution trouvée avec cette construction")