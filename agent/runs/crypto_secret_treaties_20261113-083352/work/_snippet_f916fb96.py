# Essayons d'utiliser l'outil mh_trapdoor_search
# On va appeler l'outil avec les fichiers pubkey.txt et ciphertext.txt

# Mais d'abord, on doit s'assurer que l'outil est disponible.
# Regardons les outils disponibles.

import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print("Fichiers dans le workdir:")
print(result.stdout)

# Essayons d'appeler l'outil mh_trapdoor_search
# Mais d'abord, on doit vérifier si l'outil est disponible.
# On peut utiliser run_python pour appeler l'outil.

# Pour l'instant, essayons de créer un outil personnalisé pour chercher la trapdoor.
# L'approche: pour chaque m, on calcule w = m^{-1} mod n pour différentes valeurs de n,
# et on vérifie si la séquence (pubkey * w) mod n est super-croissante.

# Mais d'abord, on doit trouver une borne pour n.
# n doit être > max(pubkey). Et n doit être tel que m * w = 1 mod n.
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
# Pour l'instant, essayons une recherche de m avec une borne plus élevée.
# Mais cette fois, on va aussi essayer de trouver n en utilisant une approche différente.

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

# Une idée différente: on peut essayer de trouver la séquence private directement en résolvant
# le subset-sum pour chaque ciphertext, puis en déduisant m et n.
#
# Pour l'instant, essayons d'utiliser l'outil mh_trapdoor_search avec une borne plus élevée.

# D'abord, vérifions si l'outil mh_trapdoor_search est disponible en listant les outils.