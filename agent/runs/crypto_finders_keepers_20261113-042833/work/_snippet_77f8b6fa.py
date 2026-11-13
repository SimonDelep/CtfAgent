encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
target_prefix = "csaw{"

# Essayons de trouver la clé XOR
for i in range(len(target_prefix)):
    xor_val = ord(encoded[i]) ^ ord(target_prefix[i])
    print(f"Position {i}: '{encoded[i]}' ^ '{target_prefix[i]}' = {xor_val} (0x{xor_val:02x})")