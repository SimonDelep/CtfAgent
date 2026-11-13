import binascii

with open('csirac/session.bin', 'rb') as f:
    data = f.read()

print(f"Taille: {len(data)} bytes")
print("Premiers 100 bytes (hex):")
print(binascii.hexlify(data[:100]).decode())

# Chercher le motif 0x81 suivi d'un caractère ASCII
print("\n--- Recherche de 0x81 ---")
for i, b in enumerate(data):
    if b == 0x81:
        if i+1 < len(data):
            next_byte = data[i+1]
            if 32 <= next_byte <= 126:
                print(f"Pos {i}: 0x81 0x{next_byte:02x} = '{chr(next_byte)}'")