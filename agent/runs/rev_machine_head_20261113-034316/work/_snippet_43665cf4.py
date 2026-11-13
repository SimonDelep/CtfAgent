import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Trouver la section .text (adresse virtuelle 0x10c0, offset 0x10c0 car c'est un PIE mais l'offset devrait correspondre)
# Pour un ELF, l'offset est dans les en-têtes de programme

# D'abord, trouvons les en-têtes de programme
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]  # Offset des en-têtes de programme
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]  # Taille d'une entrée
e_phnum = struct.unpack('<H', data[0x38:0x3a])[0]  # Nombre d'entrées

print(f"e_phoff: {hex(e_phoff)}, e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")

# Trouver la section .text
for i in range(e_phnum):
    offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[offset:offset+4])[0]
    p_offset = struct.unpack('<I', data[offset+4:offset+8])[0]
    p_vaddr = struct.unpack('<Q', data[offset+8:offset+16])[0]
    p_filesz = struct.unpack('<I', data[offset+16:offset+20])[0]
    p_memsz = struct.unpack('<I', data[offset+20:offset+24])[0]
    p_flags = struct.unpack('<I', data[offset+24:offset+28])[0]
    
    if p_type == 1:  # PT_LOAD
        print(f"LOAD segment: offset={hex(p_offset)}, vaddr={hex(p_vaddr)}, filesz={hex(p_filesz)}, flags={p_flags}")