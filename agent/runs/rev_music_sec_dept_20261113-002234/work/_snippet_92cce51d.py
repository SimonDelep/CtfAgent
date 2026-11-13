with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Les données chiffrées sont entre offset 136 et 182
encrypted = data[136:182]
salt = b's4lt26'

print(f"Encrypted ({len(encrypted)} bytes): {encrypted.hex()}")
print(f"Salt: {salt}")

# Tenter XOR avec le salt répétitif
decrypted = []
for i, b in enumerate(encrypted):
    decrypted.append(b ^ salt[i % len(salt)])

decrypted_bytes = bytes(decrypted)
print(f"\nDécrypté (XOR avec salt): {decrypted_bytes}")

# Essayer de trouver le pattern csaw{
# Le format du flag est csaw{...}
# Donc après flag{, on devrait avoir le contenu du flag et }
print(f"\nEn ASCII: {decrypted_bytes.decode('latin-1', errors='replace')}")