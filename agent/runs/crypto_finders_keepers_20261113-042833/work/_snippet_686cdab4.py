# Essayons de voir si c'est un chiffrement affine
# Pour un chiffrement affine : E(x) = (ax + b) mod 26
# Pour décoder : D(x) = a^(-1) * (x - b) mod 26

# Si e -> c et s -> s, alors :
# e (4) -> c (2) : (a*4 + b) mod 26 = 2
# s (18) -> s (18) : (a*18 + b) mod 26 = 18

# De la deuxième équation : a*18 + b = 18 mod 26
# Donc b = 18 - 18a mod 26

# Substituons dans la première :
# a*4 + (18 - 18a) = 2 mod 26
# 4a + 18 - 18a = 2 mod 26
# -14a = -16 mod 26
# 14a = 16 mod 26

# Résolvons 14a = 16 mod 26
# gcd(14, 26) = 2, et 2 divise 16, donc il y a des solutions
# 14a = 16 mod 26 => 7a = 8 mod 13
# a = 8 * 7^(-1) mod 13
# 7^(-1) mod 13 = 2 (car 7*2 = 14 = 1 mod 13)
# a = 8 * 2 = 16 = 3 mod 13

# Donc a = 3 ou a = 3 + 13 = 16 mod 26
# Si a = 3 : b = 18 - 18*3 = 18 - 54 = -36 = 16 mod 26
# Si a = 16 : b = 18 - 18*16 = 18 - 288 = -270 = 16 mod 26

# Vérifions avec a=3, b=16 :
# e (4) -> (3*4 + 16) mod 26 = 28 mod 26 = 2 = c ✓
# s (18) -> (3*18 + 16) mod 26 = 70 mod 26 = 18 = s ✓
# n (13) -> (3*13 + 16) mod 26 = 55 mod 26 = 3 = d (pas a)

# Hmm, ça ne donne pas a pour n. Essayons a=16, b=16 :
# n (13) -> (16*13 + 16) mod 26 = 224 mod 26 = 16 = q (pas a)

# Donc ce n'est pas un chiffrement affine simple

# Essayons autre chose : peut-être que c'est un décalage basé sur la position
print("Test de décalage basé sur la position:")
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
for shift in range(26):
    decoded = ""
    for i, c in enumerate(encrypted):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            # Décalage basé sur la position
            decoded += chr((ord(c) - base - shift) % 26 + base)
        else:
            decoded += c
    if decoded.startswith("csaw"):
        print(f"Shift {shift}: {decoded}")

# Ou peut-être que le décalage est basé sur l'index modulo quelque chose
print("\nTest avec décalage positionnel:")
for base_shift in range(26):
    decoded = ""
    for i, c in enumerate(encrypted):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = (base_shift + i) % 26
            decoded += chr((ord(c) - base - shift) % 26 + base)
        else:
            decoded += c
    if decoded.startswith("csaw"):
        print(f"Base shift {base_shift}: {decoded}")