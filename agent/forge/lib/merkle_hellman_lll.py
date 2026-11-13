SCHEMA = {
  "name": "merkle_hellman_lll",
  "description": "Résout le problème Merkle-Hellman subset-sum en utilisant LLL pour trouver le vecteur binaire correspondant au message",
  "parameters": {
    "properties": {
      "ciphertext_file": {
        "description": "Chemin du fichier de ciphertext",
        "type": "string"
      },
      "pubkey_file": {
        "description": "Chemin du fichier de clé publique",
        "type": "string"
      }
    },
    "required": [
      "pubkey_file",
      "ciphertext_file"
    ],
    "type": "object"
  }
}

import math

def read_integers(filename):
    """Lit les entiers d'un fichier, ignore les lignes commençant par #"""
    integers = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                integers.append(int(line))
    return integers

def lll_reduce(matrix, delta=0.99):
    """Implémentation LLL basique en pur Python"""
    n = len(matrix)
    if n == 0:
        return matrix
    
    # Gram-Schmidt
    def gram_schmidt(M):
        n = len(M)
        if n == 0:
            return []
        m = len(M[0])
        Q = [[0.0] * m for _ in range(n)]
        mu = [[0.0] * n for _ in range(n)]
        for i in range(n):
            Q[i] = [x for x in M[i]]
            for j in range(i):
                dot = sum(Q[i][k] * Q[j][k] for k in range(m))
                mu[i][j] = dot / sum(Q[j][k] * Q[j][k] for k in range(m)) if sum(Q[j][k] * Q[j][k] for k in range(m)) != 0 else 0
                for k in range(m):
                    Q[i][k] -= mu[i][j] * Q[j][k]
        return Q, mu
    
    # Initialisation
    B = [row[:] for row in matrix]
    Q, mu = gram_schmidt(B)
    
    k = 1
    while k < n:
        # Trouver le plus petit indice j >= k-1 tel que ||B_j|| > 0
        j = k - 1
        while j < n - 1 and sum(Q[j][x] * Q[j][x] for x in range(len(Q[j]))) == 0:
            j += 1
        
        if j >= n - 1:
            k += 1
            continue
        
        # Condition de Lovasz
        norm_k_minus_1 = sum(Q[k-1][x] * Q[k-1][x] for x in range(len(Q[k-1])))
        norm_k = sum(Q[k][x] * Q[k][x] for x in range(len(Q[k])))
        
        if norm_k + mu[k][k-1]**2 * norm_k_minus_1 >= delta * norm_k_minus_1:
            # Réduction
            for i in range(k-1, -1, -1):
                r = round(mu[k][i])
                if r != 0:
                    for x in range(len(B[k])):
                        B[k][x] -= r * B[i][x]
                    # Recalculer Q et mu
                    Q, mu = gram_schmidt(B)
            k += 1
        else:
            # Échange
            B[k], B[k-1] = B[k-1], B[k]
            Q, mu = gram_schmidt(B)
            k = max(k - 1, 1)
    
    return B

def solve_subset_sum_lll(pubkey, ciphertext):
    """
    Résout le problème subset-sum en utilisant LLL.
    Construit un réseau où le vecteur solution est court.
    """
    n = len(pubkey)
    
    # Construire la matrice du réseau
    # On utilise une approche où on cherche un vecteur binaire x tel que sum(pubkey[i] * x[i]) = ciphertext
    # La matrice est de dimension (n+1) x (n+1)
    
    # Matrice de base pour LLL:
    # [ 1  0  0 ... 0  pubkey[0] ]
    # [ 0  1  0 ... 0  pubkey[1] ]
    # ...
    # [ 0  0  0 ... 1  pubkey[n-1] ]
    # [ 0  0  0 ... 0  ciphertext ]
    
    # En fait, on veut trouver x tel que sum(pubkey[i] * x[i]) = ciphertext
    # On construit une matrice où le vecteur solution est (x_0, x_1, ..., x_{n-1}, -1)
    # et la dernière colonne est la contrainte
    
    # Approche: matrice de taille (n+1) x (n+1)
    # Les premières n lignes ont un 1 sur la diagonale et pubkey[i] dans la dernière colonne
    # La dernière ligne a ciphertext dans la dernière colonne et 0 ailleurs
    
    # En fait, pour trouver x binaire, on peut utiliser:
    # [ I_n | pubkey ]
    # [ 0   | ciphertext ]
    # Et chercher un vecteur court qui correspond à (x, -1)
    
    # Construction de la matrice
    size = n + 1
    matrix = [[0] * size for _ in range(size)]
    
    # Les n premières lignes: 1 sur la diagonale, pubkey[i] dans la dernière colonne
    for i in range(n):
        matrix[i][i] = 1
        matrix[i][n] = pubkey[i]
    
    # Dernière ligne: ciphertext dans la dernière colonne
    matrix[n][n] = ciphertext
    
    # Appliquer LLL
    reduced = lll_reduce(matrix)
    
    # Chercher un vecteur qui a des entrées 0 ou 1 (sauf peut-être la dernière)
    for row in reduced:
        # Vérifier si c'est un vecteur binaire valide
        binary_part = row[:n]
        if all(x == 0 or x == 1 for x in binary_part):
            # Vérifier la somme
            total = sum(pubkey[i] for i in range(n) if binary_part[i] == 1)
            if total == ciphertext:
                return binary_part
    
    return None

def bits_to_bytes(bits):
    """Convertit une liste de bits (MSB first) en bytes"""
    result = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits += [0] * (8 - len(byte_bits))
        byte_val = 0
        for b in byte_bits:
            byte_val = (byte_val << 1) | b
        result.append(byte_val)
    return bytes(result)

def main(args):
    pubkey_file = args.get('pubkey_file', 'pubkey.txt')
    ciphertext_file = args.get('ciphertext_file', 'ciphertext.txt')
    
    # Lire les données
    pubkey = read_integers(pubkey_file)
    ciphertexts = read_integers(ciphertext_file)
    
    print(f"Clé publique: {len(pubkey)} éléments")
    print(f"Nombre de blocs chiffrés: {len(ciphertexts)}")
    
    # Résoudre chaque bloc
    flag_bytes = []
    for i, ct in enumerate(ciphertexts):
        print(f"\nBloc {i+1}: {ct}")
        solution = solve_subset_sum_lll(pubkey, ct)
        if solution:
            print(f"  Solution trouvée: {sum(solution)} bits à 1")
            flag_bytes.extend(solution)
        else:
            print(f"  Solution non trouvée pour ce bloc")
            flag_bytes.extend([0] * len(pubkey))
    
    # Convertir les bits en bytes
    flag = bits_to_bytes(flag_bytes)
    print(f"\nFlag brut: {flag}")
    print(f"Flag décodé: {flag.decode('utf-8', errors='replace')}")
    
    return flag.decode('utf-8', errors='replace')

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
