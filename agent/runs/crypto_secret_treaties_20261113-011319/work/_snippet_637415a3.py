import numpy as np
from math import sqrt

def lll_reduce(M, delta=0.99):
    """LLL reduction using numpy (integer arithmetic)"""
    M = M.copy()
    n = M.shape[0]
    
    # Gram-Schmidt orthogonalisation
    def gs_orthogonalization(B):
        n = B.shape[0]
        B_star = np.zeros((n, B.shape[1]), dtype=float)
        mu = np.zeros((n, n), dtype=float)
        
        for i in range(n):
            B_star[i] = B[i].astype(float)
            for j in range(i):
                mu[i, j] = np.dot(B[i].astype(float), B_star[j]) / np.dot(B_star[j], B_star[j])
                B_star[i] = B_star[i] - mu[i, j] * B_star[j]
        return B_star, mu
    
    B_star, mu = gs_orthogonalization(M)
    
    k = 1
    while k < n:
        # Lovasz condition
        if np.dot(B_star[k], B_star[k]) >= (delta - mu[k, k-1]**2) * np.dot(B_star[k-1], B_star[k-1]):
            k += 1
        else:
            # Swap k and k-1
            M[[k-1, k]] = M[[k, k-1]]
            B_star, mu = gs_orthogonalization(M)
            k = max(k-1, 1)
    
    return M

def solve_subsetsum_lattice(pubkey, target):
    """Solve subset-sum using lattice reduction"""
    n = len(pubkey)
    
    # Build the lattice matrix
    # We want to find x such that sum(pubkey[i] * x[i]) = target
    # where x[i] in {0, 1}
    
    # Construction: (n+1) x (n+1) matrix
    # First n rows: identity with -pubkey in last column
    # Last row: 0s with 1 in last column
    
    # Actually, a better construction for subset-sum:
    # Create matrix where we look for short vector (x_0, ..., x_{n-1}, 1)
    # such that sum(x_i * pubkey[i]) = target
    
    # Matrix: for each i in 0..n-1: row i has 1 at position i, and pubkey[i] at position n
    # Last row: 0s except 1 at position n
    # Then the vector (x_0, ..., x_{n-1}, -1) gives sum(x_i * pubkey[i]) - target = 0
    
    # Alternative construction (more standard):
    # Matrix of size (n+1) x (n+1):
    # For i < n: M[i][i] = 1, M[i][n] = -pubkey[i]
    # M[n][n] = 1, M[n][j] = 0 for j < n
    # Then (x_0, ..., x_{n-1}, 1) * M = (x_0, ..., x_{n-1}, target - sum(x_i * pubkey[i]))
    # We want target - sum = 0, so sum = target
    
    # Scale to make the problem work better
    # We need to balance the magnitude of pubkey values
    
    # Let's try a different construction:
    # Use the "embedding" technique
    # Matrix size (n+1) x (n+1)
    # For i < n: M[i][i] = 1, M[i][n] = 0
    # M[n][i] = pubkey[i] for i < n, M[n][n] = -target
    # Then (x_0, ..., x_{n-1}, 1) dot product with last row gives sum(x_i * pubkey[i]) - target
    
    # Actually, let's use the standard construction for subset-sum:
    # Create a lattice where the solution is a short vector
    # Matrix: (n+1) x (n+1)
    # For i < n: M[i][i] = 1, M[i][n] = -pubkey[i]
    # M[n][n] = 1, M[n][j] = 0 for j < n
    # The vector v = (x_0, x_1, ..., x_{n-1}, 1) should satisfy v * M = (x_0, x_1, ..., x_{n-1}, target - sum)
    # We want sum = target, so the last component should be 0
    
    # Hmm, let me think again...
    # If we have M as above, and v = (x_0, ..., x_{n-1}, 1), then:
    # v * M = (x_0, x_1, ..., x_{n-1}, sum(x_i * (-pubkey[i])) + 1)
    # = (x_0, ..., x_{n-1}, 1 - sum(x_i * pubkey[i]))
    # We want sum(x_i * pubkey[i]) = target, so 1 - target should be the last component
    # That doesn't work directly.
    
    # Better construction:
    # M[i][i] = 1 for i < n
    # M[i][n] = pubkey[i] for i < n
    # M[n][j] = 0 for j < n, M[n][n] = 1
    # Then (x_0, ..., x_{n-1}, -1) * M = (x_0, ..., x_{n-1}, sum(x_i * pubkey[i]) - 1)
    # We want sum = target, so we need sum - 1 = 0, i.e., sum = 1. That's not right either.
    
    # Let me use the construction from the literature:
    # For subset-sum with target T and weights w_1, ..., w_n:
    # Create matrix of size (n+1) x (n+1):
    # For i = 1..n: M[i][i] = 1, M[i][n+1] = w_i
    # M[n+1][j] = 0 for j = 1..n, M[n+1][n+1] = T
    # Then the vector (x_1, ..., x_n, -1) has norm sqrt(sum x_i^2 + 1) = sqrt(k + 1) where k is number of 1s
    # And (x_1, ..., x_n, -1) * M = (x_1, ..., x_n, sum(x_i * w_i) - T)
    # We want sum(x_i * w_i) = T, so the last component is 0.
    
    # So the construction is:
    # M is (n+1) x (n+1)
    # For i < n: M[i][i] = 1, M[i][n] = pubkey[i]
    # M[n][j] = 0 for j < n, M[n][n] = target
    # Then (x_0, ..., x_{n-1}, -1) * M = (x_0, ..., x_{n-1}, sum(x_i * pubkey[i]) - target)
    # We want sum = target, so last component is 0.
    
    # But we need to find a short vector in the lattice. The vector (x_0, ..., x_{n-1}, -1) 
    # has length sqrt(sum x_i^2 + 1) which is at most sqrt(n + 1).
    # Other vectors might be shorter, so we need to ensure this is the shortest.
    
    # For low density subset-sum, this works because the solution is unusually short.
    
    # Build matrix
    M = np.zeros((n + 1, n + 1), dtype=object)
    for i in range(n):
        M[i, i] = 1
        M[i, n] = pubkey[i]
    M[n, n] = target
    
    # Convert to integer matrix
    M_int = np.array([[int(x) for x in row] for row in M], dtype=np.int64)
    
    print(f"Matrix shape: {M_int.shape}")
    print(f"Matrix norm of last row: {np.linalg.norm(M_int[n])}")
    
    return M_int

# Test with first ciphertext
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

print(f"First ciphertext: {ciphertexts[0]}")
M = solve_subsetsum_lattice(pubkey, ciphertexts[0])
print(f"Matrix:\n{M}")