import capstone

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# L'entrée est à l'adresse virtuelle 0x1230
# Pour un PIE, il faut trouver le décalage
# L'offset dans le fichier correspond à l'adresse virtuelle pour les segments LOAD

# Trouver l'offset du code à l'adresse 0x1230
# D'abord, regardons les segments
import struct

# Parser les en-têtes de programme
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]
e_phnum = struct.unpack('<H', data[0x38:0x3A])[0]

print(f"e_phoff: {e_phoff}, e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")

# Lire les segments
for i in range(e_phnum):
    offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[offset:offset+4])[0]
    p_offset = struct.unpack('<Q', data[offset+8:offset+16])[0]
    p_vaddr = struct.unpack('<Q', data[offset+16:offset+24])[0]
    p_filesz = struct.unpack('<Q', data[offset+32:offset+40])[0]
    p_memsz = struct.unpack('<Q', data[offset+40:offset+48])[0]
    p_flags = struct.unpack('<I', data[offset+44:offset+48])[0]
    
    if p_type == 1:  # PT_LOAD
        print(f"LOAD: offset={p_offset:#x}, vaddr={p_vaddr:#x}, filesz={p_filesz:#x}, memsz={p_memsz:#x}")
