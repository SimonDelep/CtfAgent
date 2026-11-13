import capstone
import struct

# Charger le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Parse ELF header pour trouver les segments/sections
# ELF64 header est aux premiers octets
e_type = struct.unpack('<H', data[16:18])[0]
e_machine = struct.unpack('<H', data[18:20])[0]
e_entry = struct.unpack('<Q', data[24:32])[0]
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

print(f"Entry point: 0x{e_entry:x}")
print(f"e_phoff: 0x{e_phoff:x}, e_phnum: {e_phnum}")
print(f"e_shoff: 0x{e_shoff:x}, e_shnum: {e_shnum}")

# Trouver la section enccode
# Lire les en-têtes de sections
shstrtab_offset = None
for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name_offset = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_offset_data = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    
    # Trouver le nom de la section
    if shstrtab_offset is None:
        # On doit d'abord trouver le shstrtab
        pass
    
    if sh_type == 3:  # SHT_STRTAB
        if i == e_shstrndx:
            shstrtab_offset = sh_offset_data

# Maintenant lire les noms de sections
sections = []
for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name_offset = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_offset_data = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    
    # Lire le nom
    name_start = shstrtab_offset + sh_name_offset
    name_end = data.find(b'\x00', name_start)
    name = data[name_start:name_end].decode('utf-8', errors='ignore')
    
    sections.append({
        'name': name,
        'type': sh_type,
        'addr': sh_addr,
        'offset': sh_offset_data,
        'size': sh_size
    })
    
    if 'enccode' in name:
        print(f"Section {name}: addr=0x{sh_addr:x}, offset=0x{sh_offset_data:x}, size={sh_size}")

# Trouver la section .text aussi
for s in sections:
    if s['name'] == '.text':
        print(f".text: addr=0x{s['addr']:x}, offset=0x{s['offset']:x}, size={s['size']}")