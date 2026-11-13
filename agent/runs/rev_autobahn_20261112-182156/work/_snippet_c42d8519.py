import struct

with open('nitro', 'rb') as f:
    data = f.read()

# Parser les sections
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

# Lire la chaîne des noms de sections
shstrtab_offset = struct.unpack('<Q', data[e_shoff + e_shstrndx * e_shentsize + 24: e_shoff + e_shstrndx * e_shentsize + 32])[0]
shstrtab_size = struct.unpack('<Q', data[e_shoff + e_shstrndx * e_shentsize + 32: e_shoff + e_shstrndx * e_shentsize + 40])[0]
shstrtab = data[shstrtab_offset:shstrtab_offset + shstrtab_size]

print("Section names:")
for i in range(e_shnum):
    sh_offset = struct.unpack('<Q', data[e_shoff + i * e_shentsize + 24: e_shoff + i * e_shentsize + 32])[0]
    sh_size = struct.unpack('<Q', data[e_shoff + i * e_shentsize + 32: e_shoff + i * e_shentsize + 40])[0]
    sh_type = struct.unpack('<I', data[e_shoff + i * e_shentsize + 4: e_shoff + i * e_shentsize + 8])[0]
    sh_flags = struct.unpack('<Q', data[e_shoff + i * e_shentsize + 8: e_shoff + i * e_shentsize + 16])[0]
    sh_addr = struct.unpack('<Q', data[e_shoff + i * e_shentsize + 16: e_shoff + i * e_shentsize + 24])[0]
    name_offset = struct.unpack('<I', data[e_shoff + i * e_shentsize + 0: e_shoff + i * e_shentsize + 4])[0]
    name = shstrtab[name_offset:].split(b'\x00')[0].decode('utf-8', errors='replace')
    
    if name in ['enccode', '.text', '.data', '.rodata']:
        print(f"  {name}: offset={sh_offset:#x}, size={sh_size}, addr={sh_addr:#x}, type={sh_type}, flags={sh_flags:#x}")