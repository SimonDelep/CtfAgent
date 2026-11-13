SCHEMA = {
  "name": "mh_lll_custom",
  "description": "Résout Merkle-Hellman subset-sum avec LLL en construisant une matrice appropriée et en cherchant le vecteur court correspondant au message binaire",
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

def main(args):
    import numpy as np
    from fractions import Fraction

    def lll_reduce(matrix, delta=0.99):
        """LLL réduction de base"""
        n = len(matrix)
        m = len(matrix[0])
        
        # Convertir en Fraction pour précision
        B = [[Fraction(x) for x in row] for row in matrix]
        
        # Gram-Schmidt
        def gs(B):
            n = len(B)
            m = len(B[0])
            B_star = [[Fraction(0) for _ in range(m)] for _ in range(n)]
            mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            
            for i in range(n):
                for j in range(m):
                    B_star[i][j] = B[i][j]
                
                for k in range(i):
                    mu[i][k] = Fraction(0)
                    for j in range(m):
                        mu[i][k] += B[i][j] * B_star[k][j]
                    for j in range(m):
                        B_star[i][j] -= mu[i][k] * B_star[k][j]
            
            return B_star, mu
        
        B_star, mu = gs(B)
        
        # Vérifier si vecteur est nul
        def is_zero(v):
            return all(x == 0 for x in v)
        
        def norm_sq(v):
            return sum(x*x for x in v)
        
        k = 1
        while k < n:
            # Lovasz condition
            B_star, mu = gs(B)
            
            if is_zero(B_star[k-1]):
                k += 1
                continue
                
            lhs = norm_sq(B_star[k-1])
            rhs = (delta - mu[k][k-1]**2) * norm_sq(B_star[k-1]) if k > 0 else Fraction(1)
            
            if k == 0 or lhs <= rhs:
                # Swap
                B[k], B[k-1] = B[k-1], B[k]
                k = max(k-1, 1)
            else:
                # Size reduction
                for j in range(k-1, -1, -1):
                    mu_val = mu[k][j]
                    if mu_val > Fraction(1, 2):
                        q = int(mu_val)
                        for idx in range(m):
                            B[k][idx] -= q * B[j][idx]
                k += 1
        
        # Convertir back à int
        result = []
        for row in B:
            result.append([int(x) for x in row])
        
        return result

    def solve_subsetsum_lll(pubkey, ciphertext):
        """Résout subset-sum avec LLL"""
        n = len(pubkey)
        
        # Construire matrice: on cherche (b1, ..., bn, -1) tel que sum(bi * ai) = S
        matrix = []
        for i in range(n):
            row = [0] * (n + 1)
            row[i] = 1
            row[n] = pubkey[i]
            matrix.append(row)
        
        # Dernière ligne: [0, 0, ..., 0, S]
        last_row = [0] * n + [ciphertext]
        matrix.append(last_row)
        
        # LLL réduire
        reduced = lll_reduce(matrix)
        
        # Chercher un vecteur avec dernière composante -1 ou 1
        for row in reduced:
            if row[-1] == -1 or row[-1] == 1:
                # Extraire les bits
                bits = row[:n]
                # Vérifier si c'est binaire
                if all(b in [0, 1, -1] for b in bits):
                    # Convertir en bits positifs
                    if row[-1] == -1:
                        bits = [-b for b in bits]
                    return bits
        
        return None

    # Lire les données
    pubkey = []
    with open(args['pubkey_file'], 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                pubkey.append(int(line))

    ciphertexts = []
    with open(args['ciphertext_file'], 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                ciphertexts.append(int(line))

    print(f"Pubkey length: {len(pubkey)}")
    print(f"Number of ciphertexts: {len(ciphertexts)}")

    # Essayer de résoudre chaque ciphertext
    results = []
    for i, ct in enumerate(ciphertexts):
        print(f"\nSolving ciphertext {i+1}: {ct}")
        bits = solve_subsetsum_lll(pubkey, ct)
        if bits:
            print(f"  Bits found: {bits[:10]}...")
            # Convertir bits en bytes
            # 72 bits = 9 bytes, MSB-first
            message = []
            for j in range(0, 72, 8):
                byte_bits = bits[j:j+8]
                byte_val = 0
                for b in byte_bits:
                    byte_val = byte_val * 2 + b
                message.append(byte_val)
            try:
                msg_str = bytes(message).decode('utf-8', errors='replace')
                print(f"  Message: {msg_str}")
            except:
                print(f"  Message bytes: {message}")
            results.append((bits, message))
        else:
            print(f"  No solution found")
            results.append((None, None))

    print(f"\nResults: {results}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
