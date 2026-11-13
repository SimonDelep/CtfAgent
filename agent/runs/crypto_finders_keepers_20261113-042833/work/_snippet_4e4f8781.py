# Peut-être que "esnp" est un mot clé ou un acronyme
# Essayons de voir si c'est un anagramme ou quelque chose

# "esnp" -> peut-être "pens" (pensées) ou "spen" ?
# Ou peut-être que c'est "csaw" décalé d'une certaine manière

# Regardons les XOR à nouveau : 6, 0, 15, 7
# 6 = 0x06, 0 = 0x00, 15 = 0x0F, 7 = 0x07
# Peut-être que c'est une clé hexadécimale : 06 00 0F 07

# Ou peut-être que c'est la somme des positions des lettres
# e (4) + s (18) + n (13) + p (15) = 50
# c (2) + s (18) + a (0) + w (22) = 42

# Différence : 50 - 42 = 8

# Essayons de voir si c'est un décalage de 8 sur tout le message
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("Test décalage -8 sur tout le message:")
decoded = ""
for c in encrypted:
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        decoded += chr((ord(c) - base - 8) % 26 + base)
    else:
        decoded += c
print(decoded)

# Ou peut-être que c'est un décalage différent pour chaque lettre
# e -> c : -2
# s -> s : 0
# n -> a : -13
# p -> w : +7

# Ces valeurs : -2, 0, -13, +7
# Peut-être que c'est basé sur les lettres du mot "csaw"
# c (2), s (18), a (0), w (22)

# Si on prend les positions dans l'alphabet (0-indexed) :
# c=2, s=18, a=0, w=22
# e=4, s=18, n=13, p=15

# Différence : 4-2=2, 18-18=0, 13-0=13, 15-22=-7
# Donc pour décoder : e-2=c, s-0=s, n-13=a, p-(-7)=p+7=w

# Donc la clé de décodage est : -2, 0, -13, +7
# Ou en positif : 24, 0, 13, 7

# Essayons d'appliquer cette clé en boucle sur tout le message
key = [24, 0, 13, 7]  # Clé pour décoder
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
decoded = ""
key_idx = 0
for c in encrypted:
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        decoded += chr((ord(c) - base - key[key_idx % len(key)]) % 26 + base)
        key_idx += 1
    else:
        decoded += c
print(f"Avec clé {key}: {decoded}")