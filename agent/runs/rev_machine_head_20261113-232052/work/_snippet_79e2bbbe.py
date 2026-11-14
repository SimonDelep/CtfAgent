with open('masterkey', 'rb') as f:
    data = f.read()

rodata_offset = 0x2000
rodata_data = data[rodata_offset:rodata_offset+0x8a0]

# Afficher les données entre 0x200 et 0x800
print("Données .rodata (0x200 - 0x800):")
for i in range(0x200, 0x800, 16):
    hex_str = ' '.join(f'{b:02x}' for b in rodata_data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in rodata_data[i:i+16])
    print(f"{0x2000+i:04x}: {hex_str:<48} {ascii_str}")