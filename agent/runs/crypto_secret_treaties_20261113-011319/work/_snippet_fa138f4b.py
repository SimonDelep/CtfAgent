import time

def gram_schmidt(b):
    """Gram-Schmidt orthogonalisation - version optimisée"""
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

def lll_reduce(b, delta=0.75):
    """LLL reduction - version optimisée"""
    n = len(b)
    m = len(b[0])
    
    B = [[float(b[i][j]) for j in range(m)] for i in range(n)]
    
    mu, b_star = gram_schmidt(B)
    
    k = 1
    max_iter = 3000
    
    while k < n:
        if k > 0:
            lhs = sum(b_star[k-1][j]**2 for j in range(m))
            rhs = delta * sum(b_star[k-2][j]**2 for j in range(m))
            if lhs < rhs:
                B[k-1], B[k] = B[k], B[k-1]
                mu, b_star = gram_schmidt(B)
                k = max(1, k-1)
                continue
        
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

n = len(pubkey)
print(f"n = {n}")
print(f"First pubkey element: {pubkey[0]}")
print(f"First ciphertext: {ciphertexts[0]}")

# Mesurer le temps
start = time.time()

# Construire matrice (n+1) x (n+1)
B = [[0]*(n+1) for _ in range(n+1)]
for i in range(n):
    B[i][i] = 1
    B[i][n] = pubkey[i]
B[n][n] = ciphertexts[0]

print(f"Matrice construite en {time.time() - start:.2f}s")

# Réduire
reduced = lll_reduce(B, delta=0.75)
print(f"LLL terminé en {time.time() - start:.2f}s")

# Chercher un vecteur binaire
for i, row in enumerate(reduced):
    bits = row[:n]
    if all(b in (0, 1) for b in bits):
        computed = sum(bits[j] * pubkey[j] for j in range(n))
        if computed == ciphertexts[0]:
            print(f"Trouvé à la ligne {i}!")
            byte_vals = []
            for j in range(0, 72, 8):
                byte_bits = bits[j:j+8]
                byte_val = 0
                for b in byte_bits:
                    byte_val = byte_val * 2 + b
                byte_vals.append(byte_val)
            print(f"Bytes: {byte_vals}")
            print(f"Chars: {bytes(byte_vals)}")
            break
else:
    print("Pas trouvé de vecteur binaire valide")
    # Afficher les premières lignes
    for i, row in enumerate(reduced[:5]):
        print(f"Row {i}: {row[:5]}...")