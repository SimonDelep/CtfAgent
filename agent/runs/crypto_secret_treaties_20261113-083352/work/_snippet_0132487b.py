# Essayons une approche de recherche de trapdoor plus systématique
# Pour Merkle-Hellman, la clé publique est générée comme:
# pubkey[i] = (private[i] * m) mod n
# où private est super-croissante
#
# Pour décrypter, on calcule:
# c' = (c * w) mod n, où w = m^{-1} mod n
# Puis on résout le subset-sum avec la séquence private.
#
# La séquence private est super-croissante, donc on peut la résoudre greedily.
#
# Pour trouver la trapdoor, on doit trouver m et n tels que:
# 1. m * w = 1 mod n (w est l'inverse de m mod n)
# 2. private[i] = (pubkey[i] * w) mod n est super-croissante
#
# Une approche: pour chaque m possible, on calcule w = m^{-1} mod n pour divers n,
# et on vérifie si la séquence résultante est super-croissante.
#
# Mais n est inconnu. Cependant, on sait que n > max(pubkey).
# Et n doit être tel que pour le bon m, la séquence private est super-croissante.
#
# Une autre approche: utiliser le fait que pour une séquence super-croissante,
# le rapport entre éléments consécutifs est au moins 2.
# Donc private[i+1] >= 2 * private[i] (en pratique, souvent plus).
#
# Essayons de trouver m en utilisant cette propriété.
# Si private[i] = (pubkey[i] * w) mod n, alors:
# private[i+1] / private[i] >= 2
#
# Mais c'est compliqué car on a le modulo.
#
# Une approche plus simple: utiliser LLL pour trouver la trapdoor.
# Le problème Merkle-Hellman peut être résolu en trouvant un vecteur court dans un réseau.
#
# Pour l'instant, essayons une recherche brute-force de m avec une borne raisonnable.

import math

pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Pour trouver la trapdoor, on cherche m et w tels que:
# private[i] = (pubkey[i] * w) mod n est super-croissante
#
# Une propriété: si on connaît m, alors w = m^{-1} mod n
# Et private[i] = (pubkey[i] * w) mod n
#
# Mais on ne connaît pas n. Cependant, on peut essayer différentes valeurs de n.
# n doit être > max(pubkey) et n doit être tel que m * w = 1 mod n.
#
# Une idée: pour chaque m, on peut essayer de trouver n tel que la séquence soit super-croissante.
# Mais c'est coûteux.
#
# Une autre idée: utiliser le fait que pour une séquence super-croissante,
# la somme des éléments est < 2 * max(private).
# Donc private[71] > sum(private[0:71]).
#
# Si on suppose que private est super-croissante, alors:
# private[71] > sum(private[0:71])
# Et private[i] = (pubkey[i] * w) mod n
#
# Donc (pubkey[71] * w) mod n > sum((pubkey[i] * w) mod n for i in 0..70)
#
# C'est encore compliqué.
#
# Essayons une approche différente: utiliser LLL pour trouver un vecteur binaire
# qui correspond au message. Le problème est que LLL peut ne pas donner la solution exacte
# si la densité est trop élevée.
#
# Pour l'instant, essayons de trouver la trapdoor en testant des valeurs de m.
# On suppose que m est relativement petit (par exemple, m < 10^6).

def is_superincreasing(seq):
    """Vérifie si une séquence est super-croissante."""
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

def mod_inverse(a, m):
    """Calcule l'inverse modulaire de a mod m."""
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

# Essayons de trouver m et n
# On sait que n > max(pubkey)
max_pubkey = max(pubkey)
print(f"Max pubkey: {max_pubkey}")

# Pour chaque m, on essaie de trouver n tel que la séquence soit super-croissante.
# Mais n est inconnu. Une approche: pour chaque m, on calcule w = m^{-1} mod n
# pour différentes valeurs de n, et on vérifie si la séquence est super-croissante.

# Mais c'est très coûteux. Une idée: on peut essayer de trouver n en utilisant
# le fait que n doit être tel que m * w = 1 mod n pour un certain w.
# Donc n divise (m * w - 1) pour un certain w.
#
# Une autre approche: on peut essayer de trouver la séquence private directement
# en résolvant le subset-sum pour chaque ciphertext, puis en déduisant m et n.
#
# Pour l'instant, essayons une recherche de m avec une borne raisonnable.
# On suppose que m est dans une certaine plage.

# Une idée: si on connaît le premier message (par exemple, "csaw{xxxxx}"),
# on peut essayer de trouver m et n qui donnent cette séquence.
#
# Mais on ne connaît pas le premier message complet. On sait juste qu'il commence par "csaw{".
#
# Essayons une approche différente: utiliser LLL pour trouver la trapdoor.
# Le problème Merkle-Hellman peut être formulé comme un problème de vecteur court.
#
# Pour l'instant, essayons de trouver m en testant des valeurs.

# On sait que pour une séquence super-croissante, le rapport entre éléments consécutifs
# est au moins 2. Donc private[i+1] >= 2 * private[i].
#
# Si on suppose que private[i] = (pubkey[i] * w) mod n, alors:
# (pubkey[i+1] * w) mod n >= 2 * (pubkey[i] * w) mod n
#
# C'est une contrainte sur m et n.
#
# Pour l'instant, essayons une recherche de m avec une borne de 10^6.

print("Recherche de trapdoor...")
found = False
for m in range(2, 100000):
    # Pour chaque m, on essaie de trouver n tel que la séquence soit super-croissante.
    # Mais n est inconnu. Une approche: on peut essayer différentes valeurs de n.
    #
    # Une idée: n doit être > max(pubkey). Et n doit être tel que m * w = 1 mod n.
    # Donc w = m^{-1} mod n.
    #
    # Pour chaque n > max(pubkey), on calcule w = m^{-1} mod n, puis on vérifie
    # si la séquence (pubkey * w) mod n est super-croissante.
    #
    # Mais c'est très coûteux. Une idée: on peut essayer de trouver n en utilisant
    # le fait que n doit être tel que la séquence est super-croissante.
    #
    # Pour l'instant, on essaie une approche différente: on suppose que n est proche
    # de la somme de la clé publique ou d'une valeur raisonnable.
    pass

print("Recherche terminée (sans succès pour m < 100000)")