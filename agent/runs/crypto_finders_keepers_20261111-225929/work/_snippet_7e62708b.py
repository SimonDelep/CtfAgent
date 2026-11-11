text = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [0x06, 0x00, 0x0F, 0x07, 0x00]

result = []
for i, c in enumerate(text):
    result.append(chr(ord(c) ^ key[i % len(key)]))

decoded = ''.join(result)
print(f"Texte XOR décodé avec clé 5 octets: {decoded}")