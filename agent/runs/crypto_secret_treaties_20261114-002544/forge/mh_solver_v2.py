SCHEMA = {
  "name": "mh_solver_v2",
  "description": "Résout subset-sum Merkle-Hellman avec construction de matrice LLL optimisée et vérification",
  "parameters": {
    "properties": {
      "pubkey": {
        "items": {
          "type": "integer"
        },
        "type": "array"
      },
      "target": {
        "type": "integer"
      }
    },
    "required": [
      "pubkey",
      "target"
    ],
    "type": "object"
  }
}

def main(args):
    import numpy as np
    from fpylll import IntegerMatrix, LLL
    
    pubkey = args["pubkey"]
    target = args["target"]
    n = len(pubkey)
    
    # Construction de matrice pour SVP
    # On cherche x binaire tel que sum(pubkey[i]*x[i]) = target
    # Matrice (n+1) x (n+1):
    # [ I_n     0  ]
    # [ pubkey  C  ]
    
    C = 2**60  # Constante d'embedding
    
    # Construire matrice IntegerMatrix
    mat = IntegerMatrix(n + 1, n + 1)
    
    # Les n premières lignes: identité avec pubkey dans la dernière colonne
    for i in range(n):
        mat[i, i] = 1
        mat[i, n] = pubkey[i]
    
    # Dernière ligne: 0 partout sauf -C en dernière position
    for j in range(n):
        mat[n, j] = 0
    mat[n, n] = C
    
    # Réduire avec LLL
    try:
        LLL.reduction(mat)
        
        # Examiner les vecteurs réduits
        for i in range(n + 1):
            vec = [mat[i, j] for j in range(n + 1)]
            # Vérifier si c'est une solution potentielle
            if abs(vec[n]) == 1:
                bits = [vec[j] for j in range(n)]
                if all(b in (0, 1, -1) for b in bits):
                    computed = sum(pubkey[j] * bits[j] for j in range(n))
                    expected = target * vec[n]
                    if computed == expected:
                        print(f"Solution trouvée! Vecteur {i}: {bits}")
                        if vec[n] == -1:
                            bits = [-b for b in bits]
                        print(f"Bits normalisés: {bits}")
                        return bits
        
        print("Aucune solution évidente trouvée. Vecteurs réduits:")
        for i in range(min(5, n + 1)):
            vec = [mat[i, j] for j in range(n + 1)]
            print(f"  Vecteur {i}: last={vec[n]}, poids={sum(1 for v in vec[:n] if v != 0)}")
            
    except Exception as e:
        print(f"Erreur LLL: {e}")
    
    return None

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
