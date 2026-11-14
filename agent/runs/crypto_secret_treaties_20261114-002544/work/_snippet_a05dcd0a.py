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

def solve_subsetsum_lll(pubkey, target):
    """
    Résout subset-sum en utilisant LLL sur une matrice d'embedding.
    """
    n = len(pubkey)
    
    # Construction de matrice pour SVP
    # Matrice (n+1) x (n+1)
    C = 1  # Constante de pondération
    
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
        if abs(vec[-1]) == 1:
            bits = vec[:-1]
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
    # Afficher quelques vecteurs réduits pour debug
    print("\nPremiers vecteurs réduits:")
    for i in range(min(5, len(pubkey)+1)):
        vec = [mat[i, j] for j in range(len(pubkey)+1)]
        print(f"Vecteur {i}: last={vec[-1]}, poids={sum(1 for v in vec[:-1] if v != 0)}")