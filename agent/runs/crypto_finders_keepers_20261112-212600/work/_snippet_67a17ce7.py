# Analysons la différence entre 'n' et 'a'
# n = 110, a = 97
# 110 XOR 97 = 23 (0x17)
# Mais peut-être que la clé n'est pas XOR mais un décalage ?

# e -> c : 101 -> 99 = -2
# s -> s : 115 -> 115 = 0
# n -> a : 110 -> 97 = -13
# p -> w : 112 -> 119 = +7

# Les décalages sont: -2, 0, -13, +7
# En valeur absolue: 2, 0, 13, 7

# Peut-être que c'est une clé Vigenère ?
# Si on considère que c'est un décalage alphabétique :
# e - 2 = c
# s + 0 = s
# n - 13 = a (n=13, a=0 en 0-indexed)
# p + 7 = w (p=15, w=22, 15+7=22)

# Donc les décalages sont: -2, 0, -13, +7
# Ou en valeur positive mod 26: 24, 0, 13, 7

# Essayons de trouver un motif dans ces nombres
print("Décalages:", [-2, 0, -13, 7])
print("En mod 26:", [(-2)%26, 0%26, (-13)%26, 7%26])

# Peut-être que la clé est basée sur la position ?
# Position 0: -2
# Position 1: 0
# Position 2: -13
# Position 3: +7

# Ou peut-être que c'est XOR avec une clé qui change ?
# e XOR c = 6
# s XOR s = 0
# n XOR a = 23
# p XOR w = 7

# 6, 0, 23, 7 en binaire:
print("\nEn binaire:")
print(f"6 = {bin(6)}")
print(f"0 = {bin(0)}")
print(f"23 = {bin(23)}")
print(f"7 = {bin(7)}")

# Peut-être que la clé est "csaw" XOR "esnp" = [6, 0, 23, 7]
# Et qu'on doit appliquer cette clé de manière cyclique ?

# Mais le résultat donne 'y' au lieu de 'a' pour la 3ème lettre
# Vérifions: n XOR 23 = ?
print(f"\nn XOR 23 = {chr(ord('n') ^ 23)}")  # devrait être 'a'
print(f"ord('n') = {ord('n')}, ord('a') = {ord('a')}")
print(f"110 XOR 23 = {110 ^ 23}")  # devrait être 97

# Attends, 110 XOR 23 = 85, pas 97 !
# Donc la clé pour la 3ème position n'est pas 23
# n XOR ? = a => 110 XOR x = 97 => x = 110 XOR 97 = 23
# Vérifions: 110 XOR 23 = 85, pas 97...

print(f"\nVérification: 110 XOR 23 = {110 ^ 23}")
print(f"Pour obtenir 97 à partir de 110: 110 XOR x = 97 => x = {110 ^ 97}")

# Ah, 110 XOR 97 = 23, donc 110 XOR 23 devrait donner 97
# Mais 110 XOR 23 = 85... c'est étrange
print(f"110 XOR 97 = {110 ^ 97}")
print(f"110 XOR 23 = {110 ^ 23}")

# Attends, je me suis trompé !
# 110 XOR 97 = 23, donc si on XOR 110 avec 23, on devrait obtenir 97
# Mais 110 XOR 23 = 85...
# Vérifions avec Python directement
print(f"\nord('n') XOR ord('a') = {ord('n') ^ ord('a')}")
print(f"ord('n') XOR 23 = {ord('n') ^ 23}")