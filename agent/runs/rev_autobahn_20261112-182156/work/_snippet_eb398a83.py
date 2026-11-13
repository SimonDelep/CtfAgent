import struct

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Parse ELF header
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

# Lire la table des en-têtes de sections
shstrtab_offset = None
sections = []

for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    sh_flags = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_offset_data = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    
    sections.append({
        'name_idx': sh_name,
        'type': sh_type,
        'addr': sh_addr,
        'size': sh_size,
        'flags': sh_flags,
        'offset': sh_offset_data
    })

# Trouver shstrtab
for s in sections:
    if s['type'] == 3:  # SHT_STRTAB
        shstrtab_offset = s['offset']
        break

print(f"shstrtab_offset: {hex(shstrtab_offset)}")

# Lire les noms de sections et trouver enccode
for i, s in enumerate(sections):
    name_start = shstrtab_offset + s['name_idx']
    name_end = name_start
    while name_end < len(data) and data[name_end] != 0:
        name_end += 1
    name = data[name_start:name_end].decode('utf-8', errors='replace')
    
    if name == 'enccode':
        print(f"\n=== Section enccode ===")
        print(f"  addr: {hex(s['addr'])}")
        print(f"  size: {s['size']} ({s['size']} bytes)")
        print(f"  flags: {hex(s['flags'])}")
        print(f"  file_offset: {hex(s['offset'])}")
        
        # Extraire les bytes de enccode
        enc_data = data[s['offset']:s['offset']+s['size']]
        print(f"  First 50 bytes: {enc_data[:50].hex()}")
        print(f"  Last 50 bytes: {enc_data[-50:].hex()}")
        
        # Trouver la section .text juste avant
        for j, s2 in enumerate(sections):
            if s2['addr'] < s['addr'] and s2['type'] == 1:  # SHT_PROGBITS
                if s2['addr'] + s2['size'] == s['addr']:
                    print(f"\n=== Section juste avant enccode: {name} ===")
                    print(f"  name: {name}")
                    print(f"  addr: {hex(s2['addr'])}")
                    print(f"  size: {s2['size']}")
                    print(f"  file_offset: {hex(s2['offset'])}")
                    text_data = data[s2['offset']:s2['offset']+s2['size']]
                    print(f"  Last 100 bytes of .text: {text_data[-100:].hex()}")
