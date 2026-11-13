SCHEMA = {
  "name": "mh_trapdoor_bruteforce",
  "description": "Recherche la trapdoor (w, m) d'une clé Merkle-Hellman en testant des valeurs de m et w, puis vérifie si la séquence résultante est super-increasing",
  "parameters": {
    "properties": {
      "max_m_search": {
        "description": "Nombre maximal de valeurs de m à tester",
        "type": "integer"
      },
      "max_w_search": {
        "description": "Nombre maximal de valeurs de w à tester",
        "type": "integer"
      },
      "pubkey_file": {
        "description": "Chemin du fichier de clé publique",
        "type": "string"
      }
    },
    "required": [
      "pubkey_file",
      "max_m_search",
      "max_w_search"
    ],
    "type": "object"
  }
}

import math

def is_super_increasing(seq):
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

def mod_inverse(a, m):
    """Trouve l'inverse modulaire de a modulo m"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def main(args):
    pubkey_file = args["pubkey_file"]
    max_m_search = args["max_m_search"]
    max_w_search = args["max_w_search"]
    
    # Charger la clé publique
    with open(pubkey_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    pubkey = [int(x) for x in lines]
    
    n = len(pubkey)
    max_pubkey = max(pubkey)
    
    # Pour Merkle-Hellman, la clé publique est générée comme:
    # pubkey[i] = (w * super_increasing[i]) mod m
    # où m > 2 * sum(super_increasing)
    # et w < m, gcd(w, m) = 1
    
    # On cherche m et w tels que:
    # super_increasing[i] = (pubkey[i] * w) mod m
    # et super_increasing est super-increasing
    
    # m doit être plus grand que max(pubkey)
    # Essayons différentes valeurs de m
    
    print(f"Recherche de trapdoor pour n={n}, max_pubkey={max_pubkey}")
    
    # m doit être > max(pubkey) et typiquement > 2 * sum(super_increasing)
    # On essaie m dans une plage raisonnable
    
    found = False
    for m in range(max_pubkey + 1, max_pubkey + max_m_search):
        # Pour chaque m, on cherche w tel que w * pubkey mod m donne une séquence super-increasing
        # w doit être l'inverse de quelque chose modulo m
        
        # On peut essayer différentes valeurs de w
        for w in range(2, min(m, max_w_search + 2)):
            if math.gcd(w, m) != 1:
                continue
            
            # Calculer la séquence candidate
            try:
                seq = [(pubkey[i] * w) % m for i in range(n)]
            except:
                continue
            
            # Vérifier si c'est super-increasing
            if is_super_increasing(seq):
                print(f"TRAPDOOR TROUVÉE!")
                print(f"m = {m}")
                print(f"w = {w}")
                print(f"Séquence super-increasing: {seq[:5]}...")
                return f"m={m}, w={w}, seq={seq}"
    
    return "Aucune trapdoor trouvée"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
