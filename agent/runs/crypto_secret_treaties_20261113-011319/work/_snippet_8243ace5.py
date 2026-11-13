# Implémentation LLL pure Python (version simplifiée)
# On va utiliser l'algorithme LLL standard

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

def lll_reduce(b, delta=0.75):
    """LLL reduction"""
    n = len(b)
    m = len(b[0])
    
    # Convertir à float pour les calculs
    B = [[float(b[i][j]) for j in range(m)] for i in range(n)]
    
    mu, b_star = gram_schmidt(B)
    
    k = 1
    while k < n:
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
            mu_kj = sum(B[k][i] * b_star[j][i] for i in range(m)) / sum(b_star[j][i]**2 for i in range(m))
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

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")
print(f"Premier ciphertext: {ciphertexts[0]}")