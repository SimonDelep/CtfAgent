SCHEMA = {
  "name": "subset_sum_solver",
  "description": "Résout le problème de sous-ensemble pour un ciphertext donné en utilisant une recherche avec élagage (branch and bound). Retourne les indices des éléments sélectionnés ou None si échec.",
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

def main(args):
    pubkey = args["pubkey"]
    target = args["ciphertext"]
    n = len(pubkey)
    
    # Trier la clé publique par ordre décroissant pour une meilleure élagage
    indexed_pubkey = sorted(enumerate(pubkey), key=lambda x: -x[1])
    sorted_indices = [x[0] for x in indexed_pubkey]
    sorted_pubkey = [x[1] for x in indexed_pubkey]
    
    # Précalculer les sommes suffixes pour l'élagage
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + sorted_pubkey[i]
    
    # Recherche avec élagage
    solution = None
    
    def search(idx, current_sum, selected):
        nonlocal solution
        if solution is not None:
            return  # Déjà trouvé
        
        if current_sum == target:
            solution = selected[:]
            return
        
        if idx >= n:
            return
        
        # Élagage : si current_sum + suffix_sum[idx] < target, on ne peut pas atteindre target
        if current_sum + suffix_sum[idx] < target:
            return
        
        # Élagage : si current_sum > target, on a dépassé
        if current_sum > target:
            return
        
        # Essayer d'inclure l'élément courant
        if current_sum + sorted_pubkey[idx] <= target:
            selected.append(sorted_indices[idx])
            search(idx + 1, current_sum + sorted_pubkey[idx], selected)
            if solution is not None:
                return
            selected.pop()
        
        # Essayer de ne pas inclure l'élément courant
        search(idx + 1, current_sum, selected)
    
    search(0, 0, [])
    
    if solution is None:
        return "None"
    
    # Convertir en vecteur binaire dans l'ordre original
    bits = [0] * n
    for idx in solution:
        bits[idx] = 1
    
    return bits

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
