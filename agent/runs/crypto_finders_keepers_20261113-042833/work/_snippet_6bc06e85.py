encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
target = "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"  # Hypothèse : seule la partie "esnp" est différente

# Comparaison
for i in range(len(encoded)):
    if i < len(target):
        xor_val = ord(encoded[i]) ^ ord(target[i])
        print(f"{i}: '{encoded[i]}' -> '{target[i]}' XOR={xor_val}")