# Le texte déchiffré avec "cant" est: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}
# Essayons de voir si c'est un ROT sur le contenu entre accolades

content = "b0c_@lg@el_zu0h_pz3g3_e0_o00f"

# Essayons différents décalages ROT sur les lettres seulement
def rot_n(text, n):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            rotated = chr((ord(char) - base + n) % 26 + base)
            result.append(rotated)
        else:
            result.append(char)
    return ''.join(result)

print("Texte original:", content)
for n in range(1, 26):
    decoded = rot_n(content, n)
    print(f"ROT{n}: {decoded}")