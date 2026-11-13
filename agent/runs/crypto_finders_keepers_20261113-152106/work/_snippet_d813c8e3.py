decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayons de voir si c'est un décalage de -2 sur certaines lettres
# e -> c (-2), s -> s (0), n -> a (-13), p -> w (+7)
# Ce n'est pas cohérent

# Peut-être que c'est un décalage basé sur la position?
# Ou peut-être que le message est simplement "esnp{...}" et qu'il faut le soumettre tel quel?

# Regardons si "esnp" pourrait être "csaw" avec un décalage différent
# e (101) -> c (99) = -2
# s (115) -> s (115) = 0
# n (110) -> a (97) = -13
# p (112) -> w (119) = +7

# Peut-être que c'est un décalage qui varie: -2, 0, -13, +7
# Ou peut-être que c'est un XOR avec une clé qui change

# Essayons de décoder tout le message avec XOR en utilisant la clé déduite
ciphertext = decoded.encode()
# Clé déduite des 5 premiers caractères: [6, 0, 15, 7, 0]
# Mais cela ne donne pas un message lisible

# Peut-être que le message est simplement le texte décodé et qu'il faut le soumettre
# Essayons de voir si "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}" est le flag
print(f"Message décodé: {decoded}")

# Ou peut-être que c'est un décalage de 2 sur toutes les lettres?
result = ""
for c in decoded:
    if c.isalpha():
        base = ord('a') if c.islower() else ord('A')
        result += chr((ord(c) - base - 2) % 26 + base)
    else:
        result += c
print(f"Shift -2: {result}")

# Shift +2
result2 = ""
for c in decoded:
    if c.isalpha():
        base = ord('a') if c.islower() else ord('A')
        result2 += chr((ord(c) - base + 2) % 26 + base)
    else:
        result2 += c
print(f"Shift +2: {result2}")