# Essayons de deviner le mapping en regardant la structure
# d0c -> pourrait être "doc" ou "doc"
# @yz@gl -> ?
# mn0j -> ?
# pm3z3 -> ?
# g0 -> "go"
# o00s -> "ooss" ou "oos"

# Peut-être que c'est un décalage de chaque caractère ?
payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons un décalage de -1 sur chaque caractère alphabétique
def shift_char(c, shift):
    if c.isalpha():
        base = ord('a') if c.islower() else ord('A')
        return chr((ord(c) - base + shift) % 26 + base)
    return c

for shift in range(-5, 6):
    decoded = ""
    for c in payload:
        if c.isalpha():
            decoded += shift_char(c, shift)
        else:
            decoded += c
    print(f"Shift {shift}: {decoded}")