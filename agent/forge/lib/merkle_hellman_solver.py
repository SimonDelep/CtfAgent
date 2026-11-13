SCHEMA = {
  "name": "merkle_hellman_solver",
  "description": "Résout le problème Merkle-Hellman en utilisant LLL pour le subset-sum",
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

def main(args):
    def parse_pubkey(path):
        with open(path) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        return [int(x) for x in lines]
    
    def parse_ciphertext(path):
        with open(path) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        return [int(x) for x in lines]
    
    def is_superincreasing(seq):
        total = 0
        for x in seq:
            if x <= total:
                return False
            total += x
        return True
    
    def lll_reduce(matrix, delta=0.99):
        m = len(matrix)
        n = len(matrix[0]) if m > 0 else 0
        
        B = [[float(x) for x in row] for row in matrix]
        
        def dot(u, v):
            return sum(ui * vi for ui, vi in zip(u, v))
        
        def norm(u):
            return dot(u, u)
        
        mu = [[0.0] * m for _ in range(m)]
        B_vals = [0.0] * m
        
        for i in range(m):
            B_vals[i] = norm(B[i])
            for j in range(i):
                mu[i][j] = dot(B[i], B[j]) / B_vals[j] if B_vals[j] > 0 else 0
            for j in range(i):
                for k in range(n):
                    B[i][k] -= mu[i][j] * B[j][k]
            B_vals[i] = norm(B[i])
        
        k = 1
        while k < m:
            delta_B_k_minus_1 = delta * B_vals[k-1]
            mu_k_k_minus_1 = mu[k][k-1]
            
            if B_vals[k] + mu_k_k_minus_1 * mu_k_k_minus_1 * B_vals[k-1] < delta_B_k_minus_1:
                B[k], B[k-1] = B[k-1], B[k]
                B_vals[k], B_vals[k-1] = B_vals[k-1], B_vals[k]
                
                for i in range(m):
                    if i != k and i != k-1:
                        mu[i][k], mu[i][k-1] = mu[i][k-1], mu[i][k]
                
                for i in range(k+1, m):
                    mu[i][k-1], mu[i][k] = mu[i][k], mu[i][k-1]
                
                k = max(1, k-1)
            else:
                for j in range(k-1, -1, -1):
                    if abs(mu[k][j]) > 0.5:
                        q = round(mu[k][j])
                        for l in range(n):
                            B[k][l] -= q * B[j][l]
                
                for j in range(k):
                    mu[k][j] = dot(B[k], B[j]) / B_vals[j] if B_vals[j] > 0 else 0
                B_vals[k] = norm(B[k])
                
                k += 1
        
        return [[int(round(x)) for x in row] for row in B]
    
    def solve_subsetsum_lattice(pubkey, ciphertext):
        n = len(pubkey)
        
        mat = []
        for i in range(n):
            row = [0] * (n + 1)
            row[i] = 2
            mat.append(row)
        
        row = pubkey[:] + [-ciphertext]
        mat.append(row)
        
        reduced = lll_reduce(mat)
        
        for row in reduced:
            x = row[:-1]
            last = row[-1]
            
            if all(v in [0, 1] for v in x) and last == -1:
                total = sum(pubkey[i] * x[i] for i in range(n))
                if total == ciphertext:
                    return x
        
        return None
    
    pubkey = parse_pubkey(args['pubkey_file'])
    ciphertexts = parse_ciphertext(args['ciphertext_file'])
    
    print(f"Pubkey length: {len(pubkey)}")
    print(f"Number of ciphertexts: {len(ciphertexts)}")
    print(f"Max pubkey: {max(pubkey)}")
    print(f"Min pubkey: {min(pubkey)}")
    
    print(f"Is superincreasing: {is_superincreasing(sorted(pubkey))}")
    
    results = []
    for i, ct in enumerate(ciphertexts):
        print(f"\nSolving ciphertext {i+1}: {ct}")
        x = solve_subsetsum_lattice(pubkey, ct)
        if x:
            print(f"Found solution!")
            bits = x
            bytes_val = []
            for j in range(0, 72, 8):
                byte_bits = bits[j:j+8]
                byte_val = sum(byte_bits[k] << (7-k) for k in range(8))
                bytes_val.append(byte_val)
            print(f"Bytes: {bytes_val}")
            try:
                flag_part = bytes(bytes_val).decode('utf-8')
                print(f"Flag part: {flag_part}")
            except:
                print(f"Hex: {bytes(bytes_val).hex()}")
            results.append((x, bytes_val))
        else:
            print("No solution found with LLL")
            results.append((None, None))
    
    print(f"\nResults: {results}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
