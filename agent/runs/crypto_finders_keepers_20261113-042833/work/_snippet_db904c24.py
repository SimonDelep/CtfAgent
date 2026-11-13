# Le message complet est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On sait que esnp XOR [6,0,15,7] = csaw
# Appliquons la même clé XOR cyclique sur tout le contenu

message = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7]

result = []
for i, c in enumerate(message):
    k = key[i % len(key)]
    result.append(chr(ord(c) ^ k))

decoded = "".join(result)
print("Message XORé avec clé [6,0,15,7]:")
print(decoded)