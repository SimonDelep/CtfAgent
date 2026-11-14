import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Extraire le bytecode complet du Segment 5
# Segment 5: vaddr=0x3da0, offset=0x2da0, filesz=624
bytecode = data[0x2da0:0x2da0+624]
print(f"Bytecode length: {len(bytecode)}")
print(f"Bytecode hex (first 128 bytes): {bytecode[:128].hex()}")

# Le bytecode semble être une série d'adresses ou d'instructions
# Découpons par 8 octets (64-bit values)
print("\nDécoupage par 8 octets (valeurs 64-bit little endian):")
for i in range(0, min(64, len(bytecode)), 8):
    val = struct.unpack('<Q', bytecode[i:i+8])[0]
    print(f"  0x{i:04x}: 0x{val:016x}")