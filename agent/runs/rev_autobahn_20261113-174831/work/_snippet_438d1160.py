import struct

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Section .rodata: adresse virtuelle 0x402000, offset 0x2000
# Section enccode: adresse virtuelle 0x40130d, offset 0x130d

# Trouver l'offset de la section .rodata
# D'après readelf: .rodata est à adresse 0x402000, offset 0x2000
rodata_offset = 0x2000
rodata_size = 0xb0  # Taille indiquée dans readelf

rodata = data[rodata_offset:rodata_offset + rodata_size]
print("=== .rodata (offset 0x2000, taille 0xb0) ===")
print("Hex dump:")
for i in range(0, len(rodata), 16):
    hex_part = ' '.join(f'{b:02x}' for b in rodata[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in rodata[i:i+16])
    print(f"{0x2000 + i:08x}: {hex_part:<48} {ascii_part}")

# Chercher smc_key
print("\n=== Recherche de 'smc_key' ===")
idx = rodata.find(b'smc_key')
if idx != -1:
    print(f"Trouvé à offset relatif {idx} (absolu {rodata_offset + idx})")
    print(f"Contexte: {rodata[max(0,idx-10):idx+30].hex()}")
else:
    # Chercher dans tout le binaire
    idx = data.find(b'smc_key')
    if idx != -1:
        print(f"Trouvé dans le binaire à offset {idx}")
        print(f"Contexte: {data[max(0,idx-10):idx+30].hex()}")