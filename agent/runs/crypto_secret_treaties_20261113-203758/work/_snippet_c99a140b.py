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

def solve_subsetsum_lll(pubkey, ciphertext):
    n = len(pubkey)
    size = n + 1
    
    # Créer la matrice avec IntegerMatrix
    mat = IntegerMatrix(size, size)
    
    # Remplir la matrice - utiliser set_row ou assigner directement
    for i in range(n):
        for j in range(size):
            if i == j:
                mat[i, j] = 2 * pubkey[i]
            elif j == n:
                mat[i, j] = ciphertext
            else:
                mat[i, j] = 0
    
    for j in range(n):
        mat[n, j] = 1
    mat[n, n] = 0
    
    # Réduire avec LLL
    LLL.reduction(mat)
    
    # Chercher un vecteur avec des 0 et 1
    for i in range(size):
        row = [mat[i, j] for j in range(size)]
        # Vérifier si c'est une solution binaire
        if all(x in [0, 1, -1] for x in row[:-1]):
            x = row[:-1]
            total = sum(pubkey[j] * x[j] for j in range(n))
            if total == ciphertext:
                return x
    
    return None

# Tester sur le premier ciphertext
result = solve_subsetsum_lll(pubkey, ciphertexts[0])
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
