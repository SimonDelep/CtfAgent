import struct

with open('nitro', 'rb') as f:
    data = f.read()

e_shoff = struct.unpack('<Q', data[40:48])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

print(f"e_shoff: {hex(e_shoff)}, e_shnum: {e_shnum}, e_shstrndx: {e_shstrndx}")

# Trouver la section shstrtab (index e_shstrndx)
shstrtab_idx = e_shstrndx
sh_offset = e_shoff + shstrtab_idx * e_shentsize
shstrtab_offset = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
print(f"shstrtab file offset: {hex(shstrtab_offset)}")

# Maintenant lire toutes les sections
for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    sh_flags = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_file_offset = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    
    # Lire le nom
    name_start = shstrtab_offset + sh_name
    name_end = name_start
    while name_end < len(data) and data[name_end] != 0:
        name_end += 1
    name = data[name_start:name_end].decode('utf-8', errors='replace')
    
    if name in ['.text', 'enccode', '.init', '.fini', 'smc_key.0']:
        print(f"Section '{name}': addr={hex(sh_addr)}, size={sh_size}, flags={hex(sh_flags)}, file_off={hex(sh_file_offset)}")
