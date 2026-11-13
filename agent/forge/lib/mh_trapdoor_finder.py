SCHEMA = {
  "name": "mh_trapdoor_finder",
  "description": "Recherche la trapdoor (w, m) d'une clé Merkle-Hellman en testant des valeurs de m et w",
  "parameters": {
    "properties": {
      "ciphertext_file": {
        "type": "string"
      },
      "max_m_search": {
        "type": "integer"
      },
      "max_w_search": {
        "type": "integer"
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
    import math
    from math import gcd
    
    pubkey_file = args.get('pubkey_file', 'pubkey.txt')
    ciphertext_file = args.get('ciphertext_file', 'ciphertext.txt')
    max_m_search = args.get('max_m_search', 10000)
    max_w_search = args.get('max_w_search', 10000)
    
    # Lire la clé publique
    with open(pubkey_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    pubkey = [int(l) for l in lines]
    
    # Lire le ciphertext
    with open(ciphertext_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    ciphertext = [int(l) for l in lines]
    
    n = len(pubkey)
    max_pubkey = max(pubkey)
    
    print(f"Clé publique: {n} éléments, max = {max_pubkey}")
    print(f"Ciphertext: {len(ciphertext)} blocs")
    
    base_m = max_pubkey + 1
    
    found = False
    for m_offset in range(1, max_m_search):
        m = base_m + m_offset
        
        for w in range(1, min(m, max_w_search + 1)):
            if gcd(w, m) != 1:
                continue
            
            a = [(pubkey[i] * w) % m for i in range(n)]
            
            is_super = True
            running_sum = 0
            for val in a:
                if val <= running_sum:
                    is_super = False
                    break
                running_sum += val
            
            if is_super:
                print(f"TROUVÉ! m = {m}, w = {w}")
                
                def solve_subset_sum_super(a, target):
                    n = len(a)
                    result = [0] * n
                    remaining = target
                    for i in range(n - 1, -1, -1):
                        if remaining >= a[i]:
                            result[i] = 1
                            remaining -= a[i]
                    if remaining == 0:
                        return result
                    return None
                
                decrypted_bytes = []
                for ct in ciphertext:
                    w_inv = pow(w, -1, m)
                    c_prime = (ct * w_inv) % m
                    bits = solve_subset_sum_super(a, c_prime)
                    if bits is None:
                        print(f"Échec pour ciphertext {ct}")
                        break
                    byte_vals = []
                    for j in range(0, 72, 8):
                        byte_val = 0
                        for k in range(8):
                            if bits[j + k]:
                                byte_val |= (1 << (7 - k))
                        byte_vals.append(byte_val)
                    decrypted_bytes.extend(byte_vals)
                
                if len(decrypted_bytes) == len(ciphertext) * 9:
                    flag = bytes(decrypted_bytes).decode('utf-8', errors='replace')
                    print(f"Flag déchiffré: {flag}")
                    return flag
                
                found = True
                break
        
        if found:
            break
    
    if not found:
        print("Aucune trapdoor trouvée dans la plage de recherche")
        return None

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
