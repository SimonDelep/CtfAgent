encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# XOR avec clé positionnelle (position % 256)
result = ""
for i, c in enumerate(encoded):
    result += chr(ord(c) ^ (i % 256))
print(f"XOR position: {result}")

# XOR avec clé fixe mais différente par caractère
# Regardons les différences
print("\nDifférences entre encoded et 'csaw{...}':")
target = "csaw{"
for i in range(5):
    print(f"  '{encoded[i]}' ({ord(encoded[i])}) -> '{target[i]}' ({ord(target[i])}): diff = {ord(encoded[i]) - ord(target[i])}")