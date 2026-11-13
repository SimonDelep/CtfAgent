import struct

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Parse ELF header pour trouver les segments/sections
e_type = struct.unpack('<H', data[16:18])[0]
e_machine = struct.unpack('<H', data[18:20])[0]
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

print(f"ELF type: {e_type}, machine: {hex(e_machine)}")
print(f"e_phoff: {hex(e_phoff)}, e_shoff: {hex(e_shoff)}")
print(f"e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")
print(f"e_shentsize: {e_shentsize}, e_shnum: {e_shnum}, e_shstrndx: {e_shstrndx}")

# Trouver la section enccode
# D'abord lire la chaîne des noms de sections
shstrtab_offset = None
for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    sh_flags = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    
    if sh_type == 3:  # SHT_STRTAB
        shstrtab_offset = sh_offset
    
# Lire les noms de sections
if shstrtab_offset:
    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_name = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
        sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
        sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
        sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
        sh_flags = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
        sh_offset_data = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
        
        # Lire le nom
        name_start = shstrtab_offset + sh_name
        name_end = name_start
        while name_end < len(data) and data[name_end] != 0:
            name_end += 1
        name = data[name_start:name_end].decode('utf-8', errors='replace')
        
        if name == 'enccode':
            print(f"\n=== Section enccode ===")
            print(f"  sh_addr: {hex(sh_addr)}")
            print(f"  sh_size: {sh_size} ({sh_size} bytes)")
            print(f"  sh_flags: {hex(sh_flags)}")
            print(f"  sh_offset: {hex(sh_offset_data)}")
            
            # Extraire les bytes de enccode
            enc_start = sh_offset_data
            enc_data = data[enc_start:enc_start+sh_size]
            print(f"  First 50 bytes: {enc_data[:50].hex()}")
            print(f"  Last 50 bytes: {enc_data[-50:].hex()}")
