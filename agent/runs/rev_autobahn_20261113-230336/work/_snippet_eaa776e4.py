from capstone import *
import struct

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Header ELF - trouver l'entrée et les sections
# e_entry est à l'offset 0x18 (64-bit)
e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
print(f"Entry point: 0x{e_entry:x}")

# Trouver les headers de programme et de section
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
e_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]
e_phnum = struct.unpack('<H', data[0x38:0x3a])[0]
e_shentsize = struct.unpack('<H', data[0x3a:0x3c])[0]
e_shnum = struct.unpack('<H', data[0x3c:0x3e])[0]
e_shstrndx = struct.unpack('<H', data[0x3e:0x40])[0]

print(f"e_phoff: 0x{e_phoff:x}, e_phnum: {e_phnum}")
print(f"e_shoff: 0x{e_shoff:x}, e_shnum: {e_shnum}")

# Trouver la section .text et enccode
for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name_off = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_flags = struct.unpack('<Q', data[sh_offset+8:sh_offset+16])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_offset_data = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    
    # Nom de la section (dans .shstrtab)
    # On va juste imprimer les types intéressants
    if sh_type == 1:  # SHT_PROGBITS
        # Lire le nom depuis .shstrtab
        shstrtab_offset = None
        for j in range(e_shnum):
            j_sh_offset = e_shoff + j * e_shentsize
            j_type = struct.unpack('<I', data[j_sh_offset+4:j_sh_offset+8])[0]
            if j_type == 3:  # SHT_STRTAB
                shstrtab_offset = struct.unpack('<Q', data[j_sh_offset+24:j_sh_offset+32])[0]
                break
        
        if shstrtab_offset:
            name_start = shstrtab_offset + sh_name_off
            name_end = data.find(b'\x00', name_start)
            name = data[name_start:name_end].decode('utf-8', errors='ignore')
            print(f"Section '{name}': addr=0x{sh_addr:x}, offset=0x{sh_offset_data:x}, size={sh_size:x}, flags={sh_flags:x}")