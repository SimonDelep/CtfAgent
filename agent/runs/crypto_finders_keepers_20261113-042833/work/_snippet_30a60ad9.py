# Trouver la clé XOR pour transformer "esnp" en "csaw"
encoded_prefix = "esnp"
target_prefix = "csaw"

key = []
for i in range(len(encoded_prefix)):
    key.append(ord(encoded_prefix[i]) ^ ord(target_prefix[i]))

print(f"Clé XOR: {key}")
print(f"Clé XOR en hex: {[hex(k) for k in key]}")

# Vérifions si c'est une séquence connue
print(f"Clé XOR en chars: {[chr(k) if 32 <= k < 127 else '?' for k in key]}")