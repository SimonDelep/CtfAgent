# Comparons les caractères
decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw{"

print("Analyse des différences:")
for i, (d, e) in enumerate(zip(decoded, expected_prefix)):
    diff = ord(d) - ord(e)
    print(f"  {d} ({ord(d)}) -> {e} ({ord(e)}): diff = {diff}")

# Peut-être que c'est un XOR avec une clé ?
# Essayons de trouver la clé XOR
key = []
for d, e in zip(decoded, expected_prefix):
    key.append(ord(d) ^ ord(e))
print(f"\nClé XOR potentielle: {key}")
print(f"Clé XOR en chars: {chr(key[0])}{chr(key[1])}{chr(key[2])}{chr(key[3])}{chr(key[4])}")