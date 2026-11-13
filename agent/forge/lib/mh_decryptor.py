SCHEMA = {
  "name": "mh_decryptor",
  "description": "Décrypte les ciphertexts Merkle-Hellman en cherchant la trapdoor (w, m) et en résolvant le subset-sum pour chaque bloc",
  "parameters": {
    "properties": {
      "ciphertext_file": {
        "description": "Chemin du fichier de ciphertext",
        "type": "string"
      },
      "max_m_search": {
        "description": "Nombre maximal de valeurs de m à tester",
        "type": "integer"
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

import math
from itertools import combinations

def is_super_increasing(seq):
    """Vérifie si une séquence est super-increasing"""
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Calcule l'inverse modulaire de a mod m"""
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def read_pubkey(path):
    with open(path, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    return [int(x) for x in lines]

def read_ciphertext(path):
    with open(path, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    return [int(x) for x in lines]

def solve_subset_sum_super(super_seq, target):
    """Résout le problème subset-sum pour une séquence super-increasing (greedy)"""
    n = len(super_seq)
    result = []
    for i in range(n - 1, -1, -1):
        if target >= super_seq[i]:
            result.append(i)
            target -= super_seq[i]
    if target == 0:
        return result
    return None

def bits_to_bytes(bits, n=72):
    """Convertis une liste d'indices de bits à 1 en 9 bytes"""
    byte_array = [0] * 9
    for pos in bits:
        byte_idx = pos // 8
        bit_idx = 7 - (pos % 8)  # MSB-first
        byte_array[byte_idx] |= (1 << bit_idx)
    return bytes(byte_array)

def main(args):
    pubkey_file = args.get('pubkey_file', 'pubkey.txt')
    ciphertext_file = args.get('ciphertext_file', 'ciphertext.txt')
    max_m_search = args.get('max_m_search', 100000)
    
    pubkey = read_pubkey(pubkey_file)
    ciphertexts = read_ciphertext(ciphertext_file)
    n = len(pubkey)
    
    print(f"Clé publique: {n} éléments")
    print(f"Ciphertexts: {len(ciphertexts)} blocs")
    
    max_pub = max(pubkey)
    min_pub = min(pubkey)
    sum_pub = sum(pubkey)
    
    print(f"max(pubkey) = {max_pub}")
    print(f"min(pubkey) = {min_pub}")
    print(f"sum(pubkey) = {sum_pub}")
    
    # Pour Merkle-Hellman, m > sum(s) où s est la séquence super-increasing
    # Et pub[i] = (s[i] * w) mod m
    # Donc m doit être > max(pubkey) et probablement > sum(pubkey) / w
    
    # Une approche: chercher m et w tels que s[i] = (pub[i] * w^{-1}) mod m soit super-increasing
    
    # Pour accélérer, on peut d'abord estimer m
    # Si s est super-increasing avec s[i] >= 2^i, alors sum(s) >= 2^n - 1 = 2^72 - 1
    # Mais pub[i] = (s[i] * w) mod m, donc pub[i] < m
    # Donc m > max(pubkey)
    
    # En pratique, m est souvent un nombre premier ou un nombre avec de petits facteurs
    # Essayons de chercher m dans une plage raisonnable
    
    # Une autre approche: utiliser le fait que le flag commence par "csaw{"
    # pour contraindre la recherche
    
    # Pour l'instant, essayons une recherche brute de w et m
    # Mais m peut être très grand...
    
    # Alternative: utiliser LLL pour résoudre le subset-sum directement
    # La densité est 0.75, ce qui est < 0.94, donc LLL devrait fonctionner
    
    # Implémentons LLL en Python pur (version simplifiée)
    
    print("\nTentative de résolution par LLL...")
    
    # Pour LLL, on construit une matrice où on cherche un vecteur court
    # La matrice est de la forme:
    # [ 2  0  ...  0  pubkey[0] ]
    # [ 0  2  ...  0  pubkey[1] ]
    # ...
    # [ 0  0  ...  2  pubkey[n-1] ]
    # [ 0  0  ...  0  ciphertext  ]
    
    # Mais LLL pur Python est lent pour n=72...
    
    # Essayons une approche différente: chercher la trapdoor
    # En utilisant le fait que s[i] = (pub[i] * w^{-1}) mod m doit être super-increasing
    
    # Pour une séquence super-increasing, on a s[i] > sum(s[0..i-1])
    # Donc s[i] >= 2^i (au minimum)
    
    # Si on connaît m et w, on peut calculer s[i] = (pub[i] * w^{-1}) mod m
    # Et vérifier si s est super-increasing
    
    # Une astuce: si on connaît une partie du message, on peut contraindre la recherche
    
    # Pour l'instant, essayons de chercher m et w par brute force
    # Mais m est probablement très grand...
    
    # Alternative: utiliser l'approche de "meet-in-the-middle" pour le subset-sum
    # Ou utiliser le fait que le message est ASCII imprimable
    
    # Essayons de décrypter en supposant que le message est ASCII imprimable
    # et en utilisant une recherche avec élagage
    
    print("\nTentative de décryptage par recherche avec élagage...")
    
    # Pour chaque ciphertext, on cherche un sous-ensemble de pubkey qui somme au ciphertext
    # On utilise une recherche DFS avec élagage
    
    def solve_subset_sum_branch(pubkey, target, max_depth=None):
        """Résout le problème subset-sum par recherche DFS avec élagage"""
        n = len(pubkey)
        if max_depth is None:
            max_depth = n
        
        # Trier pubkey par ordre décroissant pour une recherche plus efficace
        indexed_pubkey = sorted(enumerate(pubkey), key=lambda x: -x[1])
        
        def dfs(idx, current_sum, selected):
            if current_sum == target:
                return selected
            if idx >= n or current_sum > target:
                return None
            
            # Élagage: si la somme restante est trop petite
            remaining = sum(x[1] for x in indexed_pubkey[idx:max_depth+idx])
            if current_sum + remaining < target:
                return None
            
            # Essayer d'inclure l'élément courant
            pos, val = indexed_pubkey[idx]
            if current_sum + val <= target:
                result = dfs(idx + 1, current_sum + val, selected + [pos])
                if result is not None:
                    return result
            
            # Essayer d'exclure l'élément courant
            return dfs(idx + 1, current_sum, selected)
        
        return dfs(0, 0, [])
    
    # Essayons de décrypter le premier ciphertext
    print(f"\nDécryptage du premier ciphertext: {ciphertexts[0]}")
    
    # La recherche DFS pure est trop lente pour n=72...
    # Essayons une approche différente: utiliser la connaissance partielle du message
    
    # Le premier bloc commence par "csaw{" (5 bytes = 40 bits)
    # On connaît les positions des bits à 1 pour ces 40 bits
    
    # Calculons la somme partielle pour les bits connus
    def get_bits_from_bytes(byte_seq):
        """Extrait les positions des bits à 1 d'une séquence de bytes (MSB-first)"""
        positions = []
        for byte_idx, byte_val in enumerate(byte_seq):
            for bit_idx in range(8):
                if (byte_val >> (7 - bit_idx)) & 1:
                    positions.append(byte_idx * 8 + bit_idx)
        return positions
    
    # "csaw{" en bytes
    known_bytes = b'csaw{'
    known_positions = get_bits_from_bytes(known_bytes)
    print(f"Positions connues (csaw{{): {known_positions}")
    
    # Calculons la somme partielle
    partial_sum = sum(pubkey[pos] for pos in known_positions)
    print(f"Somme partielle (csaw{{): {partial_sum}")
    
    # La différence est la somme des bits inconnus (positions 40-71)
    remaining_target = ciphertexts[0] - partial_sum
    print(f"Target restant: {remaining_target}")
    
    # Les positions inconnues sont 40-71 (32 positions)
    unknown_positions = list(range(40, 72))
    print(f"Positions inconnues: {unknown_positions}")
    
    # Maintenant on cherche un sous-ensemble de ces 32 positions qui somme à remaining_target
    unknown_pubkey = [(pos, pubkey[pos]) for pos in unknown_positions]
    
    # Trier par valeur décroissante
    unknown_pubkey_sorted = sorted(unknown_pubkey, key=lambda x: -x[1])
    
    print(f"Nombre de positions inconnues: {len(unknown_positions)}")
    print(f"Max de unknown_pubkey: {max(x[1] for x in unknown_pubkey)}")
    
    # Essayons une recherche DFS avec élagage
    def solve_subset_sum_limited(pubkey_list, target, max_depth=32):
        """Résout le problème subset-sum pour un sous-ensemble limité"""
        n = len(pubkey_list)
        
        def dfs(idx, current_sum, selected):
            if current_sum == target:
                return selected
            if idx >= n or current_sum > target:
                return None
            
            # Élagage: somme restante
            remaining = sum(x[1] for x in pubkey_list[idx:])
            if current_sum + remaining < target:
                return None
            
            # Essayer d'inclure
            pos, val = pubkey_list[idx]
            if current_sum + val <= target:
                result = dfs(idx + 1, current_sum + val, selected + [pos])
                if result is not None:
                    return result
            
            # Essayer d'exclure
            return dfs(idx + 1, current_sum, selected)
        
        return dfs(0, 0, [])
    
    print("Recherche du sous-ensemble pour les positions inconnues...")
    result = solve_subset_sum_limited(unknown_pubkey_sorted, remaining_target)
    
    if result is not None:
        print(f"Solution trouvée: {result}")
        # Construisons le message complet
        all_selected = known_positions + result
        message_bytes = bits_to_bytes(all_selected)
        print(f"Message partiel: {message_bytes}")
    else:
        print("Aucune solution trouvée pour le premier bloc")
    
    # Retourner les données pour analyse
    return f"partial_sum={partial_sum}, remaining_target={remaining_target}, known_positions={known_positions}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
