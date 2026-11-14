from fpylll import IntegerMatrix, LLL
from fpylll.tools.bkz import BKZ

# Charger la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Charger les ciphertexts
ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

n = len(pubkey)
target = ciphertexts[0]

print(f"n = {n}, target = {target}")

# Construction de matrice avec IntegerMatrix (supporte grands entiers)
# Dimension (n+1) x (n+1)
# On veut trouver x binaire tel que sum(pubkey[i] * x[i]) = target

# Approche : embedding avec constante C
# Matrice M de taille (n+1) x (n+1)
# M[i, i] = 1 pour i < n (identité)
# M[n, i] = pubkey[i] pour i < n
# M[n, n] = -C (ou une constante adaptée)

# Pour que la solution soit un vecteur court, on cherche un vecteur v tel que
# v = (x_0, x_1, ..., x_{n-1}, 1) où x_i est 0 ou 1
# et la norme de M*v est petite

# M*v = (x_0, x_1, ..., x_{n-1}, sum(pubkey[i]*x[i]) - C)
# Si sum(pubkey[i]*x[i]) = target, alors la dernière composante est target - C

# Pour que ce soit un vecteur court, on veut target - C ≈ 0, donc C ≈ target
# Mais si C = target, alors la dernière composante est 0 quand on a la bonne solution

# Alternative : C = 1, et on cherche un vecteur où la dernière composante est -target
# La norme serait sqrt(sum(x_i^2) + target^2) ≈ sqrt(36 + target^2) qui est très grand

# Meilleure approche : utiliser C = 1 et chercher un vecteur avec dernière composante = -target
# Mais on normalise en divisant par target ou on utilise une pondération

# Essayons avec C = 1 et on regarde les vecteurs courts
C = 1
dim = n + 1

# Créer la matrice
M = IntegerMatrix.from_list([
    [1 if i == j else 0 for j in range(dim)] for i in range(n)
] + [[pubkey[i] for i in range(n)] + [-C]])

print(f"Matrice créée, dimension {dim}x{dim}")
print(f"Dernière ligne (premières 5): {M[n, :5]}")
print(f"Dernière valeur: {M[n, n]}")

# Réduire avec LLL
try:
    LLL.reduction(M)
    print("LLL réussi")
    
    # Afficher quelques vecteurs réduits
    print("\nPremiers vecteurs de la base réduite:")
    for i in range(min(5, dim)):
        vec = [M[i, j] for j in range(dim)]
        print(f"Vecteur {i}: {vec[:10]}... (last={vec[-1]})")
        
except Exception as e:
    print(f"Erreur LLL: {e}")
