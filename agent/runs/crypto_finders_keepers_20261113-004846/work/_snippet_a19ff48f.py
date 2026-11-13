cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
plain_prefix = "csaw{"

# Analyser la différence caractère par caractère
print("Analyse caractère par caractère:")
for i in range(min(len(cipher), len(plain_prefix))):
    c = cipher[i]
    p = plain_prefix[i]
    diff = ord(c) - ord(p)
    print(f"  {c} ({ord(c)}) -> {p} ({ord(p)}), diff = {diff}")

# Peut-être que c'est un décalage constant ?
# e -> c : -2
# s -> s : 0
# n -> a : -13
# p -> w : +7
# { -> { : 0
# Pas constant...

# Essayons de voir si c'est une substitution où chaque caractère est décalé d'une valeur fixe
# ou si c'est XOR avec une clé qui change

# Autre idée : peut-être que le message est encodé en Base64 d'abord, puis XOR ?
# Ou peut-être que c'est un décalage différent pour chaque position

# Regardons la chaîne complète et essayons de trouver un pattern
print("\nChaîne complète:", cipher)
print("Longueur:", len(cipher))

# Peut-être que c'est un XOR avec une clé basée sur la position ?
# Ou une clé qui est elle-même un mot ?

# Essayons de deviner le flag en supposant que c'est un message lisible
# et que la transformation est simple

# Si on suppose que le flag contient des mots anglais, on peut essayer de deviner
# Par exemple, "the", "flag", "is", etc.

# Mais d'abord, vérifions si c'est juste un décalage de chaque caractère par sa position
print("\nDécalage par position:")
result = []
for i, c in enumerate(cipher):
    # Essayer de soustraire la position
    new_char = chr(ord(c) - i)
    result.append(new_char)
print("Soustraction de position:", ''.join(result))

result2 = []
for i, c in enumerate(cipher):
    new_char = chr(ord(c) + i)
    result2.append(new_char)
print("Addition de position:", ''.join(result2))
