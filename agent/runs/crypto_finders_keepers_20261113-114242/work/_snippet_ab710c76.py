# Le texte décodé est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On veut obtenir: csaw{...}

# Essayons de trouver la substitution complète
text = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si on suppose que c'est une substitution monoalphabétique,
# on peut essayer de deviner le mot "csaw" et voir la correspondance

# e -> c
# s -> s
# n -> a
# p -> w

# Maintenant appliquons cette substitution à tout le texte
# Mais il faut trouver la règle complète

# Essayons ROT13, ROT47, etc.
import codecs

for rot in [13, 47, 5, 7, 10, 15, 20, 21]:
    # ROT pour les lettres seulement
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + rot) % 26 + base)
        else:
            result += c
    print(f"ROT{rot}: {result}")

print()
# Essayons Atbash
atbash = ""
for c in text:
    if c.isalpha():
        base = ord('a') if c.islower() else ord('A')
        atbash += chr(base + (25 - (ord(c) - base)))
    else:
        atbash += c
print(f"Atbash: {atbash}")