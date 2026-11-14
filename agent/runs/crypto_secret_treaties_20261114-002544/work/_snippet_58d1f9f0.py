from fpylll import IntegerMatrix, LLL

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
C = 1
dim = n + 1

# Créer la matrice
# Les n premières lignes sont l'identité
# La dernière ligne contient pubkey et -C
rows = []
for i in range(n):
    row = [0] * dim
    row[i] = 1
    rows.append(row)

# Dernière ligne
last_row = pubkey + [-C]
rows.append(last_row)

M = IntegerMatrix.from_list(rows)

print(f"Matrice créée, dimension {dim}x{dim}")
print(f"Dernière ligne (premières 5): {M[n, :5]}")
print(f"Dernière valeur: {M[n, n]}")

# Réduire avec LLL
try:
    LLL.reduction(M)
    print("LLL réussi")
    
    # Afficher quelques vecteurs réduits
    print("\nPremiers vecteurs de la base réduite:")
    for i in range(min(10, dim)):
        vec = [M[i, j] for j in range(dim)]
        print(f"Vecteur {i}: last={vec[-1]}, poids={sum(1 for v in vec[:-1] if v != 0)}")
        
except Exception as e:
    print(f"Erreur LLL: {e}")
