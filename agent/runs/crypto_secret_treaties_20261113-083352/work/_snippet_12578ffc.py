# Essayons d'utiliser l'outil mh_trapdoor_search
# Mais d'abord, vérifions si on peut l'appeler

# On va créer un script qui utilise l'outil mh_trapdoor_search
# en passant les fichiers pubkey.txt et ciphertext.txt

# Mais d'abord, regardons ce que fait mh_trapdoor_search
# Il recherche la trapdoor (w, m) en testant des valeurs de m et w.

# Pour l'instant, essayons avec une borne plus élevée.
# Mais d'abord, on doit s'assurer que les fichiers sont dans le bon format.

# Vérifions le contenu des fichiers
with open('pubkey.txt', 'r') as f:
    print("pubkey.txt:")
    print(f.read()[:500])

with open('ciphertext.txt', 'r') as f:
    print("ciphertext.txt:")
    print(f.read())