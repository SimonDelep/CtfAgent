encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayer XOR avec la position
for mod in range(2, 20):
    decrypted = []
    for i, char in enumerate(encrypted):
        xor_val = i % mod
        decrypted_char = chr(ord(char) ^ xor_val)
        decrypted.append(decrypted_char)
    result = ''.join(decrypted)
    if result.startswith('csaw'):
        print(f"XOR avec position % {mod}: {result}")