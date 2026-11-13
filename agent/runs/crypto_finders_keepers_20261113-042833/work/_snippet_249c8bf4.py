# Analyser la différence entre esnp et csaw
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw"

print("Analyse XOR du préfixe:")
for i, (enc, exp) in enumerate(zip(encrypted[:4], expected_prefix)):
    xor_val = ord(enc) ^ ord(exp)
    print(f"  {enc} ^ {exp} = {xor_val:02x} ({xor_val})")

# Tester si c'est un décalage simple sur tout le message
print("\nTest ROT sur le contenu entre accolades:")
content = encrypted[4:]  # {d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
for rot in range(26):
    decoded = ""
    for c in content:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            decoded += chr((ord(c) - base + rot) % 26 + base)
        else:
            decoded += c
    print(f"ROT{rot:2d}: {decoded}")