SCHEMA = {
  "name": "mh_lll_solver",
  "description": "Résout subset-sum Merkle-Hellman avec LLL, construction de matrice d'embedding, retourne solution binaire si trouvée",
  "parameters": {
    "properties": {
      "C": {
        "description": "Constante de pondération (défaut: 1)",
        "type": "integer"
      },
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

from fpylll import IntegerMatrix, LLL

def main(args):
    pubkey = args["pubkey"]
    target = args["target"]
    C = args.get("C", 1)
    
    n = len(pubkey)
    
    # Construction de matrice pour SVP
    mat = IntegerMatrix(n + 1, n + 1)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                mat[i, j] = C
            else:
                mat[i, j] = 0
        mat[i, n] = pubkey[i]
    
    for j in range(n):
        mat[n, j] = 0
    mat[n, n] = -target
    
    # Réduire avec LLL
    LLL.reduction(mat)
    
    # Vérifier les vecteurs réduits
    for i in range(n + 1):
        vec = [mat[i, j] for j in range(n + 1)]
        # Vérifier si c'est une solution potentielle
        if abs(vec[-1]) == 1:
            bits = vec[:-1]
            s = sum(pubkey[j] * bits[j] for j in range(n))
            if s == target:
                # Convertir bits en string
                bit_str = ''.join(str(b) for b in bits)
                return f"FOUND: bits={bit_str}, vec={vec}"
    
    # Si pas de solution exacte, retourner info sur les vecteurs courts
    results = []
    for i in range(min(5, n + 1)):
        vec = [mat[i, j] for j in range(n + 1)]
        last = vec[-1]
        bits = vec[:-1]
        weight = sum(1 for b in bits if b != 0)
        # Calculer la somme
        s = sum(pubkey[j] * bits[j] for j in range(n))
        results.append(f"vec[{i}]: last={last}, weight={weight}, sum={s}, target_diff={s-target}")
    
    return "\n".join(results)

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
