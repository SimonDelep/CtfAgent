decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayons de trouver un pattern dans les différences
expected = "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"  # En supposant que seul le préfixe change

# Comparaison caractère par caractère
for i in range(len(decoded)):
    if i < len(expected):
        diff = ord(decoded[i]) ^ ord(expected[i])
        print(f"{i}: '{decoded[i]}' ^ '{expected[i]}' = {diff} (0x{diff:02x})")
    else:
        print(f"{i}: '{decoded[i]}'")