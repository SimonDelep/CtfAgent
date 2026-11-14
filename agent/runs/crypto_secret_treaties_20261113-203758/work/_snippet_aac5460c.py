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

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")

n = 72

def solve_subsetsum_lll_v2(pubkey, ciphertext):
    """
    Construction de matrice pour subset-sum:
    On cherche x binaire tel que pubkey . x = ciphertext
    
    Matrice de taille (n+1) x (n+1):
    - Les n premières lignes ont 1 sur la diagonale et pubkey[i] dans la dernière colonne
    - La dernière ligne a ciphertext partout sauf 0 à la fin
    
    Non, l'approche standard est différente.
    
    Pour subset-sum, on construit:
    M = [[1, 0, ..., 0, a_0],
         [0, 1, ..., 0, a_1],
         ...
         [0, 0, ..., 1, a_{n-1}],
         [0, 0, ..., 0, s]]
    
    Après réduction, on cherche un vecteur avec des 0 et 1 dans les premières n positions
    et dont la dernière position est 0 (ou -s).
    
    En fait, la construction correcte est:
    M = [[2*a_0, 0, ..., 0, s],
         [0, 2*a_1, ..., 0, s],
         ...
         [0, 0, ..., 2*a_{n-1}, s],
         [1, 1, ..., 1, 0]]
    
    Mais il faut aussi pénaliser les solutions non-binaires.
    
    Une autre approche: utiliser une matrice de taille (n+1) x (n+1) avec:
    - Ligne i (0..n-1): e_i (vecteur de base) avec a_i dans la dernière colonne
    - Dernière ligne: (1, 1, ..., 1, -s)
    
    Après réduction, on cherche un vecteur avec des 0 et 1.
    """
    size = n + 1
    
    # Créer la matrice
    mat = IntegerMatrix(size, size)
    
    # Construction: matrice identité avec pubkey dans la dernière colonne
    # et une dernière ligne avec 1 partout et -ciphertext
    for i in range(n):
        mat[i, i] = 1
        mat[i, n] = pubkey[i]
    
    for j in range(n):
        mat[n, j] = 1
    mat[n, n] = -ciphertext
    
    # Réduire avec LLL
    LLL.reduction(mat)
    
    # Chercher un vecteur avec des 0 et 1 dans les premières n positions
    # et dont la dernière position est 0 (ou proche de 0)
    for i in range(size):
        row = [mat[i, j] for j in range(size)]
        # Vérifier si c'est une solution binaire
        if all(x in [0, 1] for x in row[:-1]):
            x = row[:-1]
            total = sum(pubkey[j] * x[j] for j in range(n))
            if total == ciphertext:
                return x
    
    return None

# Tester sur le premier ciphertext
result = solve_subsetsum_lll_v2(pubkey, ciphertexts[0])
if result:
    print("Solution trouvée!")
    bits = result
    message = []
    for i in range(0, 72, 8):
        byte_val = 0
        for j in range(8):
            byte_val = byte_val * 2 + bits[i + j]
        message.append(byte_val)
    print(f"Message: {message}")
    print(f"ASCII: {''.join(chr(b) if 32 <= b < 127 else '?' for b in message)}")
else:
    print("Aucune solution trouvée")
    
    # Afficher quelques vecteurs réduits pour debug
    size = n + 1
    mat = IntegerMatrix(size, size)
    for i in range(n):
        mat[i, i] = 1
        mat[i, n] = pubkey[i]
    for j in range(n):
        mat[n, j] = 1
    mat[n, n] = -ciphertexts[0]
    
    LLL.reduction(mat)
    
    print("\nPremiers vecteurs réduits:")
    for i in range(min(5, size)):
        row = [mat[i, j] for j in range(size)]
        print(f"Vecteur {i}: poids Hamming = {sum(1 for x in row[:-1] if x != 0)}, dernière valeur = {row[-1]}")
