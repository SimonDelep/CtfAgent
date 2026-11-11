# Texte intermédiaire décodé en Base64
text = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Clé XOR déduite du préfixe esnp -> csaw
key = [0x06, 0x00, 0x0F, 0x07]

# Appliquer XOR sur toute la chaîne
result = []
for i, c in enumerate(text):
    result.append(chr(ord(c) ^ key[i % len(key)]))

decoded = ''.join(result)
print(f"Texte XOR décodé: {decoded}")
print(f"Longueur: {len(decoded)}")