# Peut-être que la clé est basée sur le nom du challenge "finderskeepers"
# ou sur une autre chaîne

# Essayons de trouver une clé qui transforme toute la chaîne en un texte lisible
# en supposant que le flag est de la forme csaw{...}

chiffre = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si on suppose que le flag est csaw{...}, alors la clé pour les 5 premiers chars est [6, 0, 15, 7, 0]
# Mais peut-être que la clé est différente pour le reste

# Essayons de voir si la clé est dérivée de "finderskeepers" en XOR
# ou si c'est un autre schéma

# Autre idée: peut-être que c'est un XOR avec une clé qui est la position modulo quelque chose
# ou une clé dérivée d'un PRNG

# Regardons la structure du fichier MP4 pour voir s'il y a d'autres indices
# Mais d'abord, essayons de trouver une clé qui donne un flag lisible

# Supposons que le flag contient des caractères alphanumériques et _
# Essayons de deviner le contenu

# Peut-être que la clé est simplement [6, 0, 15, 7, 0] mais appliquée différemment
# ou que c'est un XOR avec une clé qui change

# Essayons avec une clé basée sur "finderskeepers" mais en commençant à une position différente
cle = "finderskeepers"
print("Essai avec différentes positions de départ:")
for start in range(len(cle)):
    resultat = ""
    for i, c in enumerate(chiffre):
        k = cle[(start + i) % len(cle)]
        resultat += chr(ord(c) ^ ord(k))
    if resultat.startswith("csaw{"):
        print(f"  start={start}: {resultat}")

# Autre idée: peut-être que la clé est "finders" ou "keepers" seul
for cle_test in ["finders", "keepers", "find", "keep", "ers", "erskeepers"]:
    resultat = ""
    for i, c in enumerate(chiffre):
        k = cle_test[i % len(cle_test)]
        resultat += chr(ord(c) ^ ord(k))
    if resultat.startswith("csaw{"):
        print(f"Clé '{cle_test}': {resultat}")
