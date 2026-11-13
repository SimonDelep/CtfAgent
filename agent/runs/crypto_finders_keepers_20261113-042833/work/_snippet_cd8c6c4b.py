message = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7]

result = []
for i, c in enumerate(message):
    k = key[i % len(key)]
    result.append((i, c, k, chr(ord(c) ^ k)))

for i, c, k, r in result:
    if c == '@':
        print(f"Position {i}: '@' XOR {k} = '{r}' (ASCII {ord(r)})")

# Affichons tout le résultat
decoded = "".join([r for _,_,_,r in result])
print("\nMessage complet XORé:")
print(decoded)