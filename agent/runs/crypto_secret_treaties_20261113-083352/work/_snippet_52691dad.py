# Essayons une approche différente: utiliser LLL pour trouver la trapdoor.
# Le problème Merkle-Hellman peut être résolu en trouvant un vecteur court dans un réseau.
#
# Une approche: construire une matrice où le vecteur solution est court, puis utiliser LLL.
#
# Mais d'abord, essayons de comprendre la structure de la clé publique.
# Si la clé publique est générée à partir d'une séquence super-croissante,
# alors il existe m et n tels que:
# pubkey[i] = (private[i] * m) mod n
#
# Pour trouver la trapdoor, on peut essayer de trouver m et n tels que
# la séquence (pubkey * w) mod n soit super-croissante, où w = m^{-1} mod n.
#
# Une idée: on peut essayer de trouver n en utilisant le fait que
# pour une séquence super-croissante, la somme des éléments est < 2 * max(private).
# Donc private[71] > sum(private[0:71]).
#
# Si on suppose que private[i] = (pubkey[i] * w) mod n, alors:
# (pubkey[71] * w) mod n > sum((pubkey[i] * w) mod n for i in 0..70)
#
# C'est une contrainte sur n et w.
#
# Une autre approche: on peut essayer de trouver m en utilisant le fait que
# m est l'inverse de w modulo n. Donc m * w = 1 mod n.
#
# Pour l'instant, essayons une recherche de m avec une borne plus élevée.
# Mais cette fois, on va aussi essayer de trouver n en utilisant une approche différente.
#
# Une idée: n doit être tel que pour le bon m, la séquence (pubkey * w) mod n est super-croissante.
# Et n doit être > max(pubkey).
#
# On peut essayer de trouver n en utilisant le fait que n divise (m * w - 1) pour un certain w.
# Donc n est un diviseur de (m * w - 1).
#
# Pour chaque m, on peut essayer différentes valeurs de w, calculer n = (m * w - 1) / k pour un certain k,
# et vérifier si la séquence est super-croissante.
#
# Mais c'est encore très coûteux.
#
# Une idée différente: on peut essayer de trouver la séquence private directement en résolvant
# le subset-sum pour chaque ciphertext, puis en déduisant m et n.
#
# Pour l'instant, essayons d'utiliser l'outil mh_trapdoor_search avec une borne plus élevée.

# D'abord, vérifions si l'outil mh_trapdoor_search est disponible
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)