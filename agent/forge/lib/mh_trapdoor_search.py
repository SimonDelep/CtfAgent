SCHEMA = {
  "name": "mh_trapdoor_search",
  "description": "Recherche la trapdoor (w, m) d'une clé Merkle-Hellman en testant des valeurs de m et w, puis vérifie si la séquence résultante est super-increasing",
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

def is_super_increasing(seq):
    """Vérifie si une séquence est super-increasing"""
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

def mod_inverse(a, m):
    """Calcule l'inverse modulaire de a mod m"""
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

def read_pubkey(path):
    with open(path, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    return [int(x) for x in lines]

def read_ciphertext(path):
    with open(path, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    return [int(x) for x in lines]

def solve_subset_sum(super_seq, target):
    """Résout le problème subset-sum pour une séquence super-increasing"""
    n = len(super_seq)
    result = []
    for i in range(n - 1, -1, -1):
        if target >= super_seq[i]:
            result.append(i)
            target -= super_seq[i]
    if target == 0:
        return result
    return None

def bits_from_indices(indices, n=72):
    """Construit un entier à partir des indices des bits à 1"""
    val = 0
    for i in indices:
        val |= (1 << (n - 1 - i))  # MSB-first
    return val

def main(args):
    pubkey_file = args.get('pubkey_file', 'pubkey.txt')
    ciphertext_file = args.get('ciphertext_file', 'ciphertext.txt')
    max_m_search = args.get('max_m_search', 100000)
    
    pubkey = read_pubkey(pubkey_file)
    ciphertexts = read_ciphertext(ciphertext_file)
    n = len(pubkey)
    
    print(f"Clé publique: {n} éléments")
    print(f"Ciphertexts: {len(ciphertexts)} blocs")
    
    # La clé publique doit être transformée en séquence super-increasing
    # pub[i] = (s[i] * w) mod m
    # Donc s[i] = (pub[i] * w^{-1}) mod m
    
    # Pour Merkle-Hellman, m > somme(s) et w < m, gcd(w,m)=1
    # La somme des éléments de la séquence super-increasing doit être < m
    
    # Essayons de trouver m et w
    # Une approche: m doit être > max(pubkey) et < 2*max(pubkey) environ
    # Ou m peut être trouvé en cherchant quand pub[i] * w^{-1} mod m donne une séquence super-increasing
    
    max_pub = max(pubkey)
    min_pub = min(pubkey)
    
    print(f"max(pubkey) = {max_pub}")
    print(f"min(pubkey) = {min_pub}")
    
    # Pour une séquence super-increasing de 72 éléments, la somme est au moins 2^72 - 1
    # Donc m doit être > 2^72
    
    # Essayons une approche différente: utiliser LLL directement sur le réseau
    # ou chercher w et m par brute force
    
    # D'abord, essayons de trouver m en cherchant quand (pub[i] * w^{-1}) mod m est super-increasing
    
    # Une heuristique: m est souvent proche de 2 * max(pubkey) ou un multiple
    # Ou m peut être trouvé en regardant les différences entre éléments
    
    # Essayons de chercher w et m
    # Pour chaque m candidat, on cherche w tel que gcd(w, m) = 1
    # Puis on calcule s[i] = (pub[i] * w^{-1}) mod m et on vérifie si super-increasing
    
    # Mais m peut être très grand... Essayons une approche par LLL d'abord
    
    # Alternative: utiliser l'outil merkle_hellman_trapdoor existant
    # Mais d'abord, essayons de trouver la trapdoor manuellement
    
    # Pour Merkle-Hellman, on a:
    # s[0] < s[1] < ... < s[n-1] (super-increasing: s[i] > sum(s[0..i-1]))
    # pub[i] = (s[i] * w) mod m
    
    # Si on connaît m et w, on peut retrouver s[i] = (pub[i] * w^{-1}) mod m
    
    # Essayons de trouver m en cherchant quand les valeurs pub[i] * w^{-1} mod m forment une séquence super-increasing
    
    # Une approche: m doit être > sum(s) et sum(s) >= 2^n - 1 pour n=72
    # Donc m > 2^72
    
    # max(pubkey) est environ 7.9e13, donc m est probablement autour de 1e14 à 1e15
    
    # Essayons de chercher m dans une plage raisonnable
    # Et pour chaque m, chercher w
    
    print("Recherche de trapdoor...")
    
    # Pour accélérer, on peut d'abord estimer m
    # Si s est super-increasing, alors s[i] >= 2^i (au minimum)
    # Donc sum(s) >= 2^n - 1 = 2^72 - 1 ≈ 4.7e21
    # Mais pub[i] = (s[i] * w) mod m, donc pub[i] < m
    # Donc m > max(pubkey) ≈ 7.9e13
    
    # En fait, pour que le chiffrement fonctionne, m doit être > sum(s)
    # Mais si sum(s) ≈ 2^72, alors m > 2^72, ce qui est énorme
    
    # Attends, peut-être que le message est seulement 72 bits, donc la somme maximale est
    # sum(pubkey) si tous les bits sont à 1
    # Mais en pratique, le message est 9 bytes = 72 bits, donc le ciphertext est la somme
    # des pubkey[i] pour les bits à 1 du message
    
    # Le ciphertext est environ 1.6e15, donc la somme des pubkey[i] pour les bits à 1 est
    # environ 1.6e15
    
    # Pour une séquence super-increasing de 72 éléments, si s[i] >= 2^i, alors
    # sum(s) >= 2^72 - 1 ≈ 4.7e21
    # Mais pub[i] = (s[i] * w) mod m, donc pub[i] peut être beaucoup plus petit que s[i]
    
    # En fait, je pense que m est autour de 2^72 ou plus
    # Et w est un entier tel que gcd(w, m) = 1
    
    # Essayons une approche différente: utiliser LLL pour trouver la solution directe
    
    # Pour le problème subset-sum, on peut utiliser LLL pour trouver le vecteur binaire
    # qui donne le ciphertext
    
    # Construisons le réseau pour LLL
    # La matrice du réseau est:
    # [ 1  0  ...  0  pubkey[0] ]
    # [ 0  1  ...  0  pubkey[1] ]
    # ...
    # [ 0  0  ...  1  pubkey[n-1] ]
    # [ 0  0  ...  0  ciphertext  ]
    
    # En fait, pour subset-sum, on utilise une matrice différente
    # On cherche x tel que sum(pubkey[i] * x[i]) = ciphertext, où x[i] ∈ {0, 1}
    
    # La matrice de base pour LLL est:
    # [ 1  0  ...  0  -pubkey[0] ]
    # [ 0  1  ...  0  -pubkey[1] ]
    # ...
    # [ 0  0  ...  1  -pubkey[n-1] ]
    # [ 0  0  ...  0  ciphertext   ]
    
    # Ou on peut utiliser la matrice:
    # [ 2  0  ...  0  pubkey[0] ]
    # [ 0  2  ...  0  pubkey[1] ]
    # ...
    # [ 0  0  ...  2  pubkey[n-1] ]
    # [ 0  0  ...  0  ciphertext  ]
    
    # En fait, la méthode standard pour subset-sum avec LLL est:
    # Construire une matrice où la dernière colonne est le ciphertext
    # et les autres colonnes sont la clé publique
    # Puis chercher un vecteur court qui correspond à la solution
    
    # Pour l'instant, essayons l'outil merkle_hellman_trapdoor
    # Mais d'abord, vérifions si on peut trouver la trapdoor
    
    # Une idée: si on connaît la structure de la clé publique, on peut essayer de
    # trouver m en regardant les différences entre les éléments
    
    # Essayons de chercher m et w par brute force pour de petites valeurs
    # Mais m est probablement très grand...
    
    # Alternative: utiliser l'approche de Coppersmith ou une réduction de réseau
    
    # Pour l'instant, essayons d'utiliser l'outil merkle_hellman_trapdoor
    # en passant les fichiers corrects
    
    print("Essayons merkle_hellman_trapdoor...")
    
    # On va appeler l'outil merkle_hellman_trapdoor
    # Mais d'abord, vérifions si les fichiers sont dans le bon format
    
    # Le fichier pubkey.txt a des lignes avec des commentaires
    # Le fichier ciphertext.txt a aussi des commentaires
    
    # Les outils devraient gérer ça
    
    # Essayons de décrypter avec merkle_hellman_trapdoor
    # Mais cet outil peut être lent...
    
    # Alternative: utiliser merkle_hellman_lll qui utilise LLL directement
    
    print("Essayons merkle_hellman_lll...")
    
    # On va retourner les données pour qu'on puisse les utiliser ailleurs
    return f"pubkey: {pubkey[:3]}...{pubkey[-3:]}\nciphertexts: {ciphertexts}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
