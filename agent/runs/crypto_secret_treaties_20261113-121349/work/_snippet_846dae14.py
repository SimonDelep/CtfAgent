# Approche: essayer de trouver m en regardant les propriétés de la clé publique
# Pour Merkle-Hellman, m > sum(a) où a est la séquence super-increasing
# Et b[i] = (a[i] * w) mod m

# Une propriété: si on prend deux éléments b[i] et b[j], alors
# b[i] * w^{-1} mod m = a[i] et b[j] * w^{-1} mod m = a[j]
# Donc b[i] * a[j] ≡ b[j] * a[i] (mod m)

# Mais on ne connaît pas a...

# Autre approche: utiliser LLL pour trouver la trapdoor
# La matrice de base pour LLL dans Merkle-Hellman est:
# [ I  |  b ]
# [ 0  |  m ]
# où on cherche un vecteur court qui correspond à la séquence super-increasing

# Pour l'instant, essayons une recherche plus intelligente de (w, m)
# En remarquant que pour une séquence super-increasing, a[i] > sum(a[0:i])
# Donc a[n-1] > sum(a[0:n-1])

# Si on suppose que m est dans une certaine plage, on peut tester rapidement

import math
from math import gcd

with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(l) for l in lines]

n = len(pubkey)
max_pubkey = max(pubkey)
min_pubkey = min(pubkey)

print(f"Range de pubkey: [{min_pubkey}, {max_pubkey}]")
print(f"Somme de pubkey: {sum(pubkey)}")

# Pour Merkle-Hellman, m doit être > sum(a)
# Et b[i] = (a[i] * w) mod m
# Donc b[i] < m pour tout i (sauf si a[i] * w >= m)

# En fait, b[i] peut être plus grand que m si a[i] * w >= m
# Mais généralement, on choisit m > sum(a) et w < m

# Essayons de trouver m en regardant les valeurs de pubkey
# Si b[i] = (a[i] * w) mod m, alors b[i] < m ou b[i] >= m

# Une idée: si on suppose que le plus grand élément de b est proche de m,
# on peut essayer m autour de max(pubkey)

# Mais en réalité, m peut être beaucoup plus grand que max(pubkey)

# Essayons une approche différente: utiliser le fait que
# pour une séquence super-increasing, les éléments croissent exponentiellement
# Donc a[i] >= 2^i * a[0] (approximativement)

# Si on peut trouver w et m tels que (b[i] * w^{-1}) mod m forme une séquence super-increasing,
# alors on a trouvé la trapdoor.

# Optimisation: au lieu de tester tous les w pour chaque m,
# on peut d'abord trouver des candidats pour m, puis tester les w.

# Une propriété: si a est super-increasing, alors a[i] > sum(a[0:i])
# Donc a[i] >= sum(a[0:i]) + 1

# Pour la clé publique b, on a b[i] = (a[i] * w) mod m
# Donc b[i] * w^{-1} mod m = a[i]

# Si on suppose que m est tel que pour un w donné,
# (b[i] * w^{-1}) mod m est super-increasing, alors on a trouvé la trapdoor.

# Essayons une recherche avec des bornes plus intelligentes
# m doit être > sum(a), et a[i] >= 2^i * a[0]
# Donc sum(a) >= a[0] * (2^n - 1)

# Pour n=72, 2^72 est énorme, donc m doit être très grand

# En fait, pour Merkle-Hellman, la séquence super-increasing est souvent
# a[i] = 2^i (ou similaire), donc sum(a) = 2^n - 1

# Pour n=72, sum(a) ≈ 2^72 ≈ 4.7e21

# Regardons la somme de pubkey
print(f"\nSomme de pubkey: {sum(pubkey)}")
print(f"2^72 = {2**72}")

# La somme de pubkey est environ 3.18e30, ce qui est beaucoup plus grand que 2^72
# Donc m doit être encore plus grand

# En fait, b[i] = (a[i] * w) mod m, donc b[i] peut être plus petit que a[i] * w
# Si a[i] * w >= m, alors b[i] = (a[i] * w) mod m < m

# Donc m peut être plus petit que sum(a * w)

# Essayons une approche basée sur LLL
print("\nEssai d'approche LLL...")

# Pour LLL, on construit une matrice où le vecteur solution est court
# La matrice typique est:
# [ 2*b[0]  2*b[1]  ...  2*b[n-1]  1 ]
# [   0       0     ...     0      M ]
# où M est un grand nombre

# Mais pour Merkle-Hellman, on cherche la trapdoor (w, m)
# Une approche est de chercher un vecteur (x_0, x_1, ..., x_{n-1}, y) tel que
# sum(x_i * b[i]) + y * m = 0 (ou quelque chose comme ça)

# Pour l'instant, essayons une recherche plus optimisée de (w, m)
# en utilisant le fait que pour une séquence super-increasing,
# a[i] > sum(a[0:i])

# Si on teste un m et un w, on peut vérifier rapidement si la séquence est super-increasing

def is_super_increasing(seq):
    running_sum = 0
    for val in seq:
        if val <= running_sum:
            return False
        running_sum += val
    return True

# Pour accélérer, on peut d'abord trouver des candidats pour m
# en regardant les propriétés de la clé publique

# Une idée: si b[i] = (a[i] * w) mod m, alors
# b[i] * w^{-1} mod m = a[i]
# Donc b[i] * w^{-1} = a[i] + k_i * m pour certains k_i

# Si on suppose que k_i = 0 pour tous les i (c'est-à-dire que a[i] * w < m),
# alors b[i] * w^{-1} = a[i], donc a[i] = b[i] * w^{-1}

# Mais cela implique que b[i] * w^{-1} est entier, donc w^{-1} doit être tel que
# b[i] * w^{-1} est entier pour tous les i

# En pratique, k_i n'est pas toujours 0

# Essayons une recherche avec des bornes raisonnables
# m doit être > max(pubkey) (sinon b[i] mod m = b[i] pour tous les i)
# Et m doit être tel que pour un w donné, (b[i] * w^{-1}) mod m est super-increasing

# Pour accélérer, on peut d'abord trouver des candidats pour w
# en regardant les propriétés de la clé publique

# Une propriété: si a est super-increasing, alors a[i] >= 2^i * a[0]
# Donc a[n-1] >= 2^{n-1} * a[0]

# Pour n=72, a[71] >= 2^71 * a[0]

# Si on suppose que a[0] est petit (par exemple 1), alors a[71] >= 2^71

# Mais en pratique, a[0] peut être plus grand

# Essayons une recherche avec des bornes plus larges
print("\nRecherche de trapdoor avec optimisation...")

# Pour accélérer, on peut utiliser le fait que
# si (b[i] * w^{-1}) mod m est super-increasing, alors
# (b[i] * w^{-1}) mod m > sum((b[j] * w^{-1}) mod m for j < i)

# Cela signifie que pour chaque i, (b[i] * w^{-1}) mod m doit être plus grand
# que la somme de tous les précédents

# On peut vérifier cette propriété rapidement

# Pour l'instant, essayons une recherche avec des bornes raisonnables
# m dans [max(pubkey) + 1, max(pubkey) + 100000]
# w dans [1, 100000]

base_m = max_pubkey + 1
found = False

# Pour accélérer, on peut d'abord trouver des candidats pour m
# en regardant les propriétés de la clé publique

# Une idée: si on suppose que m est tel que pour un w donné,
# (b[i] * w^{-1}) mod m est super-increasing, alors
# (b[i] * w^{-1}) mod m doit être plus grand que la somme de tous les précédents

# Pour accélérer, on peut d'abord vérifier si un w donné peut fonctionner
# en regardant les propriétés de la clé publique

# Pour l'instant, essayons une recherche simple avec des bornes raisonnables
import time
start = time.time()

for m_offset in range(1, 100000):
    m = base_m + m_offset
    
    # Pour chaque m, on cherche un w tel que gcd(w, m) = 1
    # et (b[i] * w^{-1}) mod m est super-increasing
    
    # Pour accélérer, on peut d'abord trouver les w candidats
    # en regardant les propriétés de la clé publique
    
    # Une idée: si (b[i] * w^{-1}) mod m est super-increasing,
    # alors (b[i] * w^{-1}) mod m doit être plus grand que la somme de tous les précédents
    
    # Pour accélérer, on peut vérifier cette propriété pour les premiers éléments
    # avant de vérifier tous les éléments
    
    for w in range(1, 10000):
        if gcd(w, m) != 1:
            continue
        
        # Calcule w^{-1} mod m
        try:
            w_inv = pow(w, -1, m)
        except:
            continue
        
        # Calcule la séquence transformée
        a = [(pubkey[i] * w_inv) % m for i in range(n)]
        
        # Vérifie rapidement si super-increasing
        running_sum = 0
        is_super = True
        for val in a:
            if val <= running_sum:
                is_super = False
                break
            running_sum += val
        
        if is_super:
            print(f"TROUVÉ! m = {m}, w = {w}")
            print(f"Séquence super-increasing: {a[:10]}...")
            found = True
            break
    
    if found:
        break
    
    if m_offset % 10000 == 0:
        elapsed = time.time() - start
        print(f"Progression: m_offset = {m_offset}, elapsed = {elapsed:.2f}s")

if not found:
    print("Aucune trapdoor trouvée dans la plage de recherche")