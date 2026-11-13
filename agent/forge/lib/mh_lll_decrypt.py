SCHEMA = {
  "name": "mh_lll_decrypt",
  "description": "Résout Merkle-Hellman subset-sum avec LLL pour décrypter un ciphertext donné",
  "parameters": {
    "properties": {
      "ciphertext": {
        "description": "Ciphertext à décrypter",
        "type": "integer"
      },
      "pubkey": {
        "description": "Clé publique (liste d'entiers)",
        "items": {
          "type": "integer"
        },
        "type": "array"
      }
    },
    "required": [
      "pubkey",
      "ciphertext"
    ],
    "type": "object"
  }
}

import numpy as np
from fpylll import IntegerMatrix, LLL

def solve_subsetsum_lll(pubkey, ciphertext):
    n = len(pubkey)
    
    C = 1000000  # Facteur de pondération
    
    # Créer la matrice (n+1) x (n+1)
    mat = np.zeros((n + 1, n + 1), dtype=np.int64)
    
    # Partie identité
    for i in range(n):
        mat[i, i] = 1
    
    # Dernière ligne: pubkey et C
    for i in range(n):
        mat[n, i] = pubkey[i]
    mat[n, n] = C
    
    # Convertir en IntegerMatrix pour fpylll
    M = IntegerMatrix.from_array(mat)
    
    # Réduire avec LLL
    LLL.reduction(M)
    
    # Chercher le vecteur solution
    for i in range(n + 1):
        candidate = np.array(M[i])
        x = candidate[:n]
        # Essayer de convertir en binaire (arrondir)
        x_bin = np.round(x).astype(int)
        if np.all((x_bin == 0) | (x_bin == 1)):
            computed = np.sum(np.array(pubkey) * x_bin)
            if computed == ciphertext:
                return x_bin
    
    return None

def main(args):
    pubkey = args["pubkey"]
    ciphertext = args["ciphertext"]
    
    result = solve_subsetsum_lll(pubkey, ciphertext)
    if result is not None:
        print("Solution trouvée!")
        print("Vecteur binaire:", result)
        # Convertir bits en octets
        message_bytes = []
        for i in range(0, 72, 8):
            byte_bits = result[i:i+8]
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit
            message_bytes.append(byte_val)
        print("Message bytes:", message_bytes)
        try:
            message = bytes(message_bytes).decode('ascii')
            print("Message:", repr(message))
        except:
            print("Message (hex):", bytes(message_bytes).hex())
        return result
    else:
        print("Aucune solution trouvée")
        return None

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
