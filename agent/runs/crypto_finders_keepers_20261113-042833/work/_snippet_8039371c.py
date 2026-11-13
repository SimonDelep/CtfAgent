# @ est ASCII 64, _ est ASCII 95
# 64 XOR x = 95 => x = 64 XOR 95 = 31
print("@ (64) XOR 31 =", chr(64 ^ 31))  # devrait donner _

# Vérifions aussi si la clé [6,0,15,7] appliquée à @ donne _
key = [6, 0, 15, 7]
for i, k in enumerate(key):
    result = chr(64 ^ k)
    print(f"@ XOR {k} =", result, f"(ASCII {ord(result)})")

# Peut-être que @ est juste un placeholder pour _
# Et le flag est simplement csaw{d0c_yz_gl_mn0j_pm3z3_g0_o00s}
print("\nFlag potentiel: csaw{d0c_yz_gl_mn0j_pm3z3_g0_o00s}")