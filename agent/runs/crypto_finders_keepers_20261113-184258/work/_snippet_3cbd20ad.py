decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw"

# Trouver la clé XOR
key = []
for i in range(len(expected_prefix)):
    key.append(ord(decoded[i]) ^ ord(expected_prefix[i]))

print(f"Clé XOR déduite: {key}")
print(f"Clé XOR en hex: {[hex(k) for k in key]}")
print(f"Clé XOR en chars: {[chr(k) if 32 <= k < 127 else '?' for k in key]}")

# Appliquer cette clé à tout le message
result = ''
for i, c in enumerate(decoded):
    k = key[i % len(key)]
    result += chr(ord(c) ^ k)

print(f"Décodé avec clé XOR: {result}")

# Peut-être que la clé est "csaw" elle-même?
key2 = [ord(c) for c in "csaw"]
result2 = ''
for i, c in enumerate(decoded):
    k = key2[i % len(key2)]
    result2 += chr(ord(c) ^ k)

print(f"Décodé avec clé 'csaw': {result2}")