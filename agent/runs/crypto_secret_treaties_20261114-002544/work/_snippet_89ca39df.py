import numpy as np

# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

n = len(pubkey)
print(f"n = {n}")

# Pour chaque ciphertext, essayer de trouver le vecteur binaire
# Construction de lattice pour SVP:
# Matrice (n+1) x (n+1):
# [ I_n    0  ]
# [ pubkey target ]
# où target est le ciphertext

# Mais pour CVP, on peut utiliser l'embedding:
# [ I_n    0  ]
# [ pubkey -target ]
# et chercher un vecteur avec dernière coordonnée = -1

# Alternative: construction avec poids
# On veut trouver x binaire tel que pubkey.x = target
# Lattice: [ I_n  0 ]
#          [ 2*pubkey  -2*target ]
# La solution aura dernière coordonnée = -1

# Essayons une construction simple d'abord
def try_solve_ct(ct, pubkey, verbose=False):
    n = len(pubkey)
    # Construction: matrice (n+1) x (n+1)
    # L = [ I_n    0  ]
    #     [ pubkey  ct ]
    # On cherche un vecteur avec dernière coordonnée = 1
    
    # En fait, pour SVP on veut:
    # [ I_n    0  ]
    # [ pubkey  ct ]
    # et chercher un vecteur court qui a dernière coordonnée = 1
    
    # Construction standard pour subset-sum:
    # Matrice (n+1) x (n+1):
    # b_i = e_i pour i < n (vecteurs de base)
    # b_n = (pubkey_0, pubkey_1, ..., pubkey_{n-1}, ct)
    # On cherche combinaison linéaire entière avec dernière coordonnée = 1
    
    # Alternative: utiliser la construction de Lagarias-Odlyzko
    # [ I_n    0  ]
    # [ 2*pubkey  -2*ct ]
    # La solution est (x_1, ..., x_n, -1) où x_i est binaire
    
    # Essayons avec fpylll
    try:
        from fpylll import IntegerMatrix, LLL, BKZ
        from fpylll.util import gaussian_heuristic
        
        # Construction de la matrice
        # On utilise une pondération pour forcer la dernière coordonnée
        C = 1  # constante d'embedding
        
        M = IntegerMatrix(n + 1, n + 1)
        
        # Les n premières lignes: vecteurs de base avec pubkey
        for i in range(n):
            M[i, i] = 1
            M[i, n] = pubkey[i]
        
        # Dernière ligne: cible
        M[n, n] = ct
        
        if verbose:
            print(f"Matrice {M.rows}x{M.cols}")
            print(f"Première ligne: {list(M[0])}")
            print(f"Dernière ligne: {list(M[n])}")
        
        # LLL reduction
        LLL.reduction(M)
        
        # Vérifier les vecteurs réduits
        for i in range(n + 1):
            row = [M[i, j] for j in range(n + 1)]
            if row[-1] == 1 or row[-1] == -1:
                # Vérifier si c'est une solution binaire
                bits = row[:n]
                if all(b in [0, 1, -1] for b in bits):
                    # Calculer la somme
                    total = sum(pubkey[j] * bits[j] for j in range(n))
                    if verbose:
                        print(f"Vecteur trouvé: last={row[-1]}, bits={bits[:5]}...")
                    return bits, row[-1]
        
        # Si on trouve un vecteur avec last = -1, c'est potentiellement la solution
        for i in range(n + 1):
            row = [M[i, j] for j in range(n + 1)]
            if row[-1] == -1:
                bits = row[:n]
                # Vérifier si binaire
                if all(b in [0, 1] for b in bits):
                    total = sum(pubkey[j] * bits[j] for j in range(n))
                    if verbose:
                        print(f"Solution trouvée! bits binaire, last=-1")
                    return bits, -1
        
        # Sinon, retourner le vecteur le plus court
        min_len = float('inf')
        best_row = None
        for i in range(n + 1):
            row = [M[i, j] for j in range(n + 1)]
            length = sum(x*x for x in row)
            if length < min_len:
                min_len = length
                best_row = row
        
        if verbose:
            print(f"Vecteur le plus court: last={best_row[-1]}, len={min_len}")
        return best_row, best_row[-1]
        
    except Exception as e:
        if verbose:
            print(f"Erreur: {e}")
        return None, None

# Tester sur le premier ciphertext
bits, last = try_solve_ct(ciphertexts[0], pubkey, verbose=True)
print(f"Résultat: bits={bits[:10] if bits else None}, last={last}")