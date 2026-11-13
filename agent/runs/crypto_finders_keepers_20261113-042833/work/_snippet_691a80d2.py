# Test XOR cyclique avec la clé [6, 0, 15, 7] sur le payload
payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
key = [6, 0, 15, 7]

result = []
for i, c in enumerate(payload):
    k = key[i % len(key)]
    result.append(chr(ord(c) ^ k))

print("XOR cyclique avec clé [6,0,15,7]:")
print("".join(result))
print()

# Testons aussi avec @ = espace (32)
print("Si @ = espace (32):")
payload2 = payload.replace("@", " ")
print(payload2)