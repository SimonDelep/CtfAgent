import numpy as np

# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

n = len(pubkey)

# Tester avec fpylll
try:
    from fpylll import IntegerMatrix, LLL, BKZ
    
    # Créer une matrice
    M = IntegerMatrix(n + 1, n + 1)
    
    # Remplir la matrice
    for i in range(n):
        M[i, i] = 1
        M[i, n] = pubkey[i]
    
    M[n, n] = ciphertexts[0]
    
    print(f"Type M: {type(M)}")
    print(f"Dir M: {[x for x in dir(M) if not x.startswith('_')]}")
    
except Exception as e:
    import traceback
    traceback.print_exc()