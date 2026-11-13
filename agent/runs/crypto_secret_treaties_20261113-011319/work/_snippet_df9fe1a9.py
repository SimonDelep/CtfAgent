def gram_schmidt(b):
    """Gram-Schmidt orthogonalisation"""
    n = len(b)
    m = len(b[0])
    mu = [[0.0] * n for _ in range(n)]
    b_star = [[0.0] * m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            b_star[i][j] = b[i][j]
        for j in range(i):
            s = sum(b_star[i][k] * b_star[j][k] for k in range(m))
            t = sum(b_star[j][k] * b_star[j][k] for k in range(m))
            if t > 0:
                mu[i][j] = s / t
            for k in range(m):
                b_star[i][k] -= mu[i][j] * b_star[j][k]
    
    return mu, b_star

def lll_reduce(b, delta=0.99):
    """LLL reduction avec delta proche de 1 pour plus de force"""
    n = len(b)
    m = len(b[0])
    
    # Convertir à float pour les calculs
    B = [[float(b[i][j]) for j in range(m)] for i in range(n)]
    
    mu, b_star = gram_schmidt(B)
    
    k = 1
    max_iter = 10000
    iter_count = 0
    
    while k < n and iter_count < max_iter:
        iter_count += 1
        # Lovasz condition
        if k > 0:
            lhs = sum(b_star[k-1][j]**2 for j in range(m))
            rhs = delta * sum(b_star[k-2][j]**2 for j in range(m))
            if lhs < rhs:
                # Swap k-1 et k
                B[k-1], B[k] = B[k], B[k-1]
                mu, b_star = gram_schmidt(B)
                k = max(1, k-1)
                continue
        
        # Size reduction
        for j in range(k-1, -1, -1):
            denom = sum(b_star[j][i]**2 for i in range(m))
            if denom > 0:
                mu_kj = sum(B[k][i] * b_star[j][i] for i in range(m)) / denom
                q = round(mu_kj)
                for i in range(m):
                    B[k][i] -= q * B[j][i]
        
        mu, b_star = gram_schmidt(B)
        k += 1
    
    return [[int(round(x)) for x in row] for row in B]

# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

n = len(pubkey)  # 72

# Construire la matrice pour LLL
# Matrice (n+1) x (n+1)
# Les premières n lignes ont un 1 sur la diagonale et a[i] dans la dernière colonne
# La dernière ligne a c dans la dernière colonne

def solve_subsetsum(pubkey, ciphertext):
    n = len(pubkey)
    
    # Construire la matrice
    # On utilise une approche différente: matrice avec -1 pour le ciphertext
    # [ I_n | a ]
    # [ 0   | c ]
    # Après réduction, on cherche un vecteur court
    
    # Alternative: matrice avec scaling
    # On construit: [ I_n  a ]
    #               [ 0    c ]
    # Et on cherche un vecteur (x, -sum) où x est binaire
    
    # Version standard: 
    # B = [ I_n  a ]
    #     [ 0    c ]
    # Le vecteur solution est (x, -c) où x est le vecteur binaire
    
    # En fait, on veut trouver x tel que sum(x[i]*a[i]) = c
    # Donc sum(x[i]*a[i]) - c = 0
    # Le vecteur (x, -1) donne: x*a + (-1)*c = 0
    
    # Construire matrice (n+1) x (n+1)
    B = [[0]*(n+1) for _ in range(n+1)]
    
    for i in range(n):
        B[i][i] = 1
        B[i][n] = pubkey[i]
    
    B[n][n] = ciphertext
    
    # Réduire avec LLL
    reduced = lll_reduce(B, delta=0.99)
    
    # Chercher un vecteur avec des entrées 0/1 dans les premières n positions
    for row in reduced:
        # Vérifier si c'est un vecteur binaire (0 ou 1) dans les premières n positions
        bits = row[:n]
        if all(b in (0, 1) for b in bits):
            # Vérifier que la somme correspond
            computed = sum(bits[i] * pubkey[i] for i in range(n))
            if computed == ciphertext:
                return bits
    
    return None

# Essayer sur le premier ciphertext
bits = solve_subsetsum(pubkey, ciphertexts[0])
if bits:
    print("Trouvé!")
    print(f"Bits: {bits[:20]}...")
    # Convertir en bytes (9 bytes = 72 bits, MSB-first)
    byte_vals = []
    for i in range(0, 72, 8):
        byte_bits = bits[i:i+8]
        byte_val = 0
        for b in byte_bits:
            byte_val = byte_val * 2 + b
        byte_vals.append(byte_val)
    print(f"Bytes: {byte_vals}")
    print(f"Chars: {bytes(byte_vals)}")
else:
    print("Pas trouvé directement, essayons une approche différente")