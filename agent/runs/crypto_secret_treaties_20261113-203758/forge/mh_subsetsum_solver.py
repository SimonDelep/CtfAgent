SCHEMA = {
  "name": "mh_subsetsum_solver",
  "description": "Résout le problème subset-sum Merkle-Hellman en testant plusieurs constructions de matrice LLL/BKZ. Retourne le vecteur binaire trouvé ou None.",
  "parameters": {
    "properties": {
      "ciphertext": {
        "type": "integer"
      },
      "method": {
        "enum": [
          "lagarias",
          "cvp",
          "bkz"
        ],
        "type": "string"
      },
      "pubkey": {
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
from fpylll import IntegerMatrix, LLL, BKZ

def solve_lagarias(pubkey, ciphertext):
    """Construction de Lagarias-Odlyzko pour subset-sum"""
    n = len(pubkey)
    c = n + 1
    
    # Matrice de taille (n+1) x (n+1)
    # On utilise float64 pour éviter les overflow, puis on arrondit
    mat = np.zeros((n+1, n+1), dtype=np.float64)
    
    for i in range(n):
        mat[i][i] = 1.0
        mat[i][n] = float(c * pubkey[i])
    
    mat[n][n] = float(c * ciphertext)
    
    # Convertir en IntegerMatrix (fpylll gère les grands entiers via Python)
    try:
        imat = IntegerMatrix.from_matrix(mat.astype(np.int64))
    except:
        # Si overflow, utiliser une approche différente
        return None
    
    # LLL reduction
    LLL.reduction(imat)
    
    # Chercher un vecteur court avec poids de Hamming n+1 (ou proche)
    for i in range(n+1):
        row = imat[i]
        # Vérifier si c'est un vecteur binaire (ou proche)
        vec = np.array(row)
        # Le vecteur solution devrait avoir des composantes 0 ou 1 (sauf la dernière qui est -1)
        if np.all((vec[:-1] == 0) | (vec[:-1] == 1)) and vec[-1] == -1:
            return vec[:-1].astype(int)
    
    return None

def solve_cvp(pubkey, ciphertext):
    """Construction CVP simple"""
    n = len(pubkey)
    
    # Matrice: identité + colonne avec pubkey et -ciphertext
    mat = np.zeros((n+1, n+1), dtype=np.float64)
    
    for i in range(n):
        mat[i][i] = 1.0
    for i in range(n):
        mat[n][i] = float(pubkey[i])
    mat[n][n] = float(-ciphertext)
    
    try:
        imat = IntegerMatrix.from_matrix(mat.astype(np.int64))
    except:
        return None
    
    LLL.reduction(imat)
    
    for i in range(n+1):
        vec = np.array(imat[i])
        if np.all((vec[:-1] == 0) | (vec[:-1] == 1)):
            # Vérifier que sum(vec[:-1] * pubkey) == ciphertext
            if np.sum(vec[:-1].astype(int) * pubkey) == ciphertext:
                return vec[:-1].astype(int)
    
    return None

def solve_bkz(pubkey, ciphertext, block_size=20):
    """Utilise BKZ avec taille de bloc ajustable"""
    n = len(pubkey)
    
    # Construction: matrice où on cherche un vecteur court
    # Colonne i: 1 en position i, pubkey[i] en position n
    # Colonne n: 0 partout sauf -ciphertext en position n
    
    mat = np.zeros((n+1, n+1), dtype=np.float64)
    
    for i in range(n):
        mat[i][i] = 1.0
        mat[n][i] = float(pubkey[i])
    mat[n][n] = float(-ciphertext)
    
    try:
        imat = IntegerMatrix.from_matrix(mat.astype(np.int64))
    except:
        return None
    
    # BKZ reduction
    bkz = BKZ.BlockReduction(block_size=block_size)
    bkz(imat)
    
    for i in range(n+1):
        vec = np.array(imat[i])
        if np.all((vec[:-1] == 0) | (vec[:-1] == 1)):
            if np.sum(vec[:-1].astype(int) * pubkey) == ciphertext:
                return vec[:-1].astype(int)
    
    return None

def main(args):
    pubkey = args["pubkey"]
    ciphertext = args["ciphertext"]
    method = args.get("method", "lagarias")
    
    if method == "lagarias":
        result = solve_lagarias(pubkey, ciphertext)
    elif method == "cvp":
        result = solve_cvp(pubkey, ciphertext)
    elif method == "bkz":
        result = solve_bkz(pubkey, ciphertext)
    else:
        result = None
    
    if result is not None:
        return f"Found solution: {result.tolist()}"
    else:
        return "No solution found"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
