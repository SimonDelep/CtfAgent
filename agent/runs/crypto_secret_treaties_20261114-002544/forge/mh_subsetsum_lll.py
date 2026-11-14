SCHEMA = {
  "name": "mh_subsetsum_lll",
  "description": "Résout un problème subset-sum Merkle-Hellman avec LLL. Prend pubkey (liste) et target (int), retourne le vecteur binaire solution si trouvé.",
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

from fpylll import IntegerMatrix, LLL

def main(args):
    pubkey = args["pubkey"]
    target = args["target"]
    C = args.get("C", 1)
    
    n = len(pubkey)
    dim = n + 1
    
    # Créer la matrice manuellement
    M = IntegerMatrix(dim, dim)
    
    # Les n premières lignes sont l'identité
    for i in range(n):
        for j in range(dim):
            M[i, j] = 1 if i == j else 0
    
    # Dernière ligne contient pubkey et -C
    for i in range(n):
        M[n, i] = pubkey[i]
    M[n, n] = -C
    
    # Réduire avec LLL
    try:
        LLL.reduction(M)
    except Exception as e:
        return f"LLL error: {e}"
    
    # Chercher un vecteur avec dernière composante = -C (ou C) et coefficients binaires
    for i in range(dim):
        vec = [M[i, j] for j in range(dim)]
        last = vec[-1]
        
        # On cherche un vecteur où last = -C (ou C) et les autres sont 0 ou 1
        if abs(last) == C:
            # Vérifier si les autres composantes sont 0 ou 1
            prefix = vec[:-1]
            if all(v in [0, 1] for v in prefix):
                # Vérifier la somme
                computed = sum(pubkey[j] * prefix[j] for j in range(n))
                expected = target if last == -C else -target
                if computed == expected:
                    return prefix
    
    return "no binary vector found"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
