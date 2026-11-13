encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7]

# Appliquer la clé XOR répétitivement
decrypted = []
for i, char in enumerate(encrypted):
    xor_val = key[i % len(key)]
    decrypted_char = chr(ord(char) ^ xor_val)
    decrypted.append(decrypted_char)

result = ''.join(decrypted)
print(f"Résultat XOR: {result}")