with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# flag{ est à la position 124-133
# Le salt s4lt26 commence à 182
# Donc le flag est entre 134 et 182

flag_start = 134  # après le '{'
salt_start = 182

print(f"Bytes du flag potentiel (positions {flag_start} à {salt_start}):")
flag_bytes = data[flag_start:salt_start]
print(flag_bytes.hex())
print(f"Longueur: {len(flag_bytes)} bytes")

# Essayons de décoder en supposant que c'est XOR avec un motif
# D'abord, regardons si c'est XOR avec le salt répété
salt = b"s4lt26"
print(f"\nSalt: {salt}")

# Essayons XOR avec le salt répété
decoded = []
for i, b in enumerate(flag_bytes):
    xor_key = salt[i % len(salt)]
    decoded.append(b ^ xor_key)

print("\nDécodé avec XOR salt:")
print(bytes(decoded))

# Essayons aussi de trouver un motif plus simple
# Peut-être que chaque byte est XOR avec une valeur fixe
print("\n--- Tentative XOR avec valeur fixe ---")
for key in range(256):
    decoded = bytes([b ^ key for b in flag_bytes])
    # Vérifions si ça ressemble à du texte ASCII
    try:
        text = decoded.decode('ascii')
        if text.isprintable() or all(c.isalnum() or c in '_{}' for c in text):
            print(f"Key {key} (0x{key:02x}): {text}")
    except:
        pass