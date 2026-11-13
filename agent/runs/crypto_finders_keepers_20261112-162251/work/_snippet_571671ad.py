encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayer avec différentes clés
keys_to_try = ["key", "csaw", "flag", "seed", "xor", "abc", "0123"]

for key in keys_to_try:
    decrypted = []
    for i, char in enumerate(encrypted):
        xor_val = ord(key[i % len(key)])
        decrypted_char = chr(ord(char) ^ xor_val)
        decrypted.append(decrypted_char)
    result = ''.join(decrypted)
    print(f"Clé '{key}': {result}")