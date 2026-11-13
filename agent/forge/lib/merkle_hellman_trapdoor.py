SCHEMA = {
  "name": "merkle_hellman_trapdoor",
  "description": "Trouve la trapdoor (w, m) d'une clé Merkle-Hellman et décrypte les ciphertexts",
  "parameters": {
    "properties": {
      "ciphertext_file": {
        "type": "string"
      },
      "pubkey_file": {
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
from fractions import Fraction

def read_integers(filename):
    integers = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                integers.append(int(line))
    return integers

def lll_short_vector(matrix, delta=0.99):
    """LLL optimisé pour trouver un vecteur court"""
    n = len(matrix)
    if n == 0:
        return matrix, None
    
    # Gram-Schmidt avec flottants
    def gs(B):
        m = len(B[0])
        B_star = [[0.0]*m for _ in range(n)]
        mu = [[0.0]*n for _ in range(n)]
        for i in range(n):
            B_star[i] = [float(x) for x in B[i]]
            for j in range(i):
                dot = sum(B_star[i][k] * B_star[j][k] for k in range(m))
                norm_j = sum(B_star[j][k] * B_star[j][k] for k in range(m))
                if norm_j > 0:
                    mu[i][j] = dot / norm_j
                    for k in range(m):
                        B_star[i][k] -= mu[i][j] * B_star[j][k]
        return B_star, mu
    
    B = [row[:] for row in matrix]
    B_star, mu = gs(B)
    
    k = 1
    while k < n:
        # Lovasz condition
        norm_km1 = sum(B_star[k-1][x]**2 for x in range(len(B_star[k-1])))
        norm_k = sum(B_star[k][x]**2 for x in range(len(B_star[k])))
        
        if norm_k + mu[k][k-1]**2 * norm_km1 >= delta * norm_km1:
            # Reduction
            for i in range(k-1, -1, -1):
                r = round(mu[k][i])
                if r != 0:
                    for x in range(len(B[k])):
                        B[k][x] -= r * B[i][x]
            B_star, mu = gs(B)
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            B_star, mu = gs(B)
            k = max(k-1, 1)
    
    return B, None

def find_trapdoor_lll(pubkey):
    """
    Trouve la trapdoor (w, m) en utilisant LLL.
    Construit un réseau où le vecteur (w, -1) est court.
    """
    n = len(pubkey)
    
    # Construire la matrice pour trouver w
    # On utilise l'approche où on cherche un vecteur (w, -1) tel que
    # pubkey[i] * w ≡ s[i] (mod m) pour tout i
    # où s[i] est petit (super-increasing)
    
    # Matrice de taille (n+1) x (n+1):
    # [ m   0   0  ...  0  pubkey[0] ]
    # [ 0   m   0  ...  0  pubkey[1] ]
    # ...
    # [ 0   0   0  ...  m  pubkey[n-1] ]
    # [ 0   0   0  ...  0  -1        ]
    
    # En fait, on veut trouver w tel que pubkey[i] * w mod m soit petit
    # Pour cela, on construit une matrice où chaque ligne i a:
    # - m sur la diagonale
    # - pubkey[i] dans la dernière colonne
    # Et on cherche un vecteur (0, 0, ..., w, -1) qui est court
    
    # Approche simplifiée: utiliser LLL directement sur le problème subset-sum
    # avec une matrice pondérée
    
    # Pour trouver w et m, on peut utiliser une approche basée sur les GCDs
    # ou chercher m comme un diviseur commun approximatif
    
    # Pour l'instant, retournons None et essayons une autre approche
    return None, None

def solve_subset_sum_greedy(superincreasing, target):
    """Résout subset-sum pour une séquence super-increasing (algorithme glouton)"""
    n = len(superincreasing)
    result = [0] * n
    
    # Parcourir de la fin vers le début
    for i in range(n-1, -1, -1):
        if target >= superincreasing[i]:
            result[i] = 1
            target -= superincreasing[i]
    
    if target == 0:
        return result
    return None

def bits_to_text(bits):
    """Convertit une liste de bits en texte ASCII"""
    result = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits += [0] * (8 - len(byte_bits))
        byte_val = 0
        for b in byte_bits:
            byte_val = (byte_val << 1) | b
        if byte_val > 0:
            result.append(chr(byte_val))
    return ''.join(result)

def main(args):
    pubkey_file = args.get('pubkey_file', 'pubkey.txt')
    ciphertext_file = args.get('ciphertext_file', 'ciphertext.txt')
    
    pubkey = read_integers(pubkey_file)
    ciphertexts = read_integers(ciphertext_file)
    
    n = len(pubkey)
    print(f"Clé publique: {n} éléments")
    print(f"Ciphertexts: {len(ciphertexts)} blocs")
    
    # Approche: trouver w et m en cherchant un diviseur commun
    # ou utiliser LLL pour trouver un vecteur court
    
    # Pour Merkle-Hellman, on peut trouver m en cherchant un diviseur commun
    # des éléments de la clé publique, mais m est généralement plus grand
    
    # Une autre approche: utiliser LLL pour trouver directement le message
    # en construisant une matrice de taille (n+1) x (n+1)
    
    # Pour chaque ciphertext, construisons la matrice et appliquons LLL
    flag_chars = []
    
    for ct_idx, ct in enumerate(ciphertexts):
        print(f"\nBloc {ct_idx + 1}: {ct}")
        
        # Construire la matrice pour LLL
        # Matrice (n+1) x (n+1):
        # [ I_n | pubkey ]
        # [ 0   | ct     ]
        # On cherche un vecteur (x_0, ..., x_{n-1}, -1) qui est court
        
        size = n + 1
        matrix = [[0] * size for _ in range(size)]
        
        for i in range(n):
            matrix[i][i] = 1
            matrix[i][n] = pubkey[i]
        matrix[n][n] = ct
        
        # Appliquer LLL
        reduced, _ = lll_short_vector(matrix)
        
        # Chercher un vecteur binaire
        found = False
        for row in reduced:
            binary_part = row[:n]
            # Vérifier si c'est un vecteur binaire (0 ou 1)
            if all(x == 0 or x == 1 for x in binary_part):
                total = sum(pubkey[i] for i in range(n) if binary_part[i] == 1)
                if total == ct:
                    print(f"  Solution trouvée: {sum(binary_part)} bits à 1")
                    # Convertir les bits en texte
                    text = bits_to_text(binary_part)
                    print(f"  Texte: {text}")
                    flag_chars.append(text)
                    found = True
                    break
        
        if not found:
            # Afficher les premières lignes réduites pour déboguer
            print(f"  Aucune solution binaire trouvée")
            for i in range(min(3, len(reduced))):
                row = reduced[i]
                print(f"    Ligne {i}: {row[:5]}...{row[-3:]}")
    
    flag = ''.join(flag_chars)
    print(f"\nFlag: {flag}")
    return flag

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
