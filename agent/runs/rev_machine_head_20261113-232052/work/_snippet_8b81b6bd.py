import capstone

with open('masterkey', 'rb') as f:
    data = f.read()

# La section .rodata est à l'adresse virtuelle 0x2000
# Trouvons l'offset fichier correspondant

# Segment LOAD à 0x2000
# D'après l'analyse précédente: LOAD: offset=0x2000, vaddr=0x2000, filesz=0x8a0
# Donc .rodata est à offset 0x2000 dans le fichier

rodata_offset = 0x2000
rodata_data = data[rodata_offset:rodata_offset+0x8a0]

# Afficher les chaînes et les données
print("Données .rodata (hex):")
for i in range(0, min(0x200, len(rodata_data), 16)):
    hex_str = ' '.join(f'{b:02x}' for b in rodata_data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in rodata_data[i:i+16])
    print(f"{0x2000+i:04x}: {hex_str:<48} {ascii_str}")