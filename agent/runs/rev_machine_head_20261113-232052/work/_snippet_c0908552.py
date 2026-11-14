with open('masterkey', 'rb') as f:
    data = f.read()

rodata_offset = 0x2000
rodata_data = data[rodata_offset:rodata_offset+0x8a0]

# Trouver la fin des données non nulles
last_nonzero = 0
for i, b in enumerate(rodata_data):
    if b != 0:
        last_nonzero = i

print(f"Dernier octet non nul à offset: {hex(last_nonzero)}")
print(f"Taille de rodata_data: {len(rodata_data)}")

# Afficher les données autour de last_nonzero
start = max(0, last_nonzero - 32)
end = min(len(rodata_data), last_nonzero + 32)
print(f"\nDonnées autour de {hex(last_nonzero)}:")
for i in range(start, end, 16):
    hex_str = ' '.join(f'{b:02x}' for b in rodata_data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in rodata_data[i:i+16])
    print(f"{0x2000+i:04x}: {hex_str:<48} {ascii_str}")