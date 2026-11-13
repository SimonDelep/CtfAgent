# Données extraites
singletons = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]
# On a besoin de tous les 112 singletons
# La clé mod 256 est [179, 168, 116, 164, 175, 183]

# Mais peut-être que les singletons doivent être traités différemment
# Essayons de voir si les singletons mod 256 XOR avec la clé donne quelque chose

# D'abord, récupérons tous les singletons
# L'outil a donné seulement les 20 premiers, on a besoin des 112

# Essayons une autre approche: peut-être que le message est dans les différences
# ou que les singletons sont déjà le message XORé avec quelque chose

# Regardons les singletons mod 256
singleton_mod256 = [s % 256 for s in [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]]
print("Singletons mod 256 (first 20):", singleton_mod256)

# La clé mod 256
key_mod256 = [179, 168, 116, 164, 175, 183]

# XOR avec la clé cyclique
result = []
for i, s in enumerate(singleton_mod256):
    result.append(s ^ key_mod256[i % 6])
print("XOR result (first 20):", bytes(result))

# Peut-être que la clé est dans un ordre différent?
# Les ports fréquents par ordre d'apparition: [40115, 40104, 40052, 40100, 40111, 40119]
# Mod 256: [179, 168, 116, 164, 175, 183]

# Essayons l'ordre inverse
key_reverse = key_mod256[::-1]
result_reverse = []
for i, s in enumerate(singleton_mod256):
    result_reverse.append(s ^ key_reverse[i % 6])
print("XOR avec clé inversée:", bytes(result_reverse))

# Peut-être que les singletons ne sont pas le message, mais qu'il faut les trier?
# Ou peut-être que le message est dans les ports fréquents eux-mêmes?
print("\nPorts fréquents mod 256:", [p % 256 for p in [40115, 40104, 40052, 40100, 40111, 40119]])