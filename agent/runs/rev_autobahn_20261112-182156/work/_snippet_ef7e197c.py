import struct

with open('nitro', 'rb') as f:
    data = f.read()

e_shoff = struct.unpack('<Q', data[40:48])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

# Trouver la section shstrtab
shstrtab_idx = e_shstrndx
sh_offset = e_shoff + shstrtab_idx * e_shentsize
shstrtab_offset = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]

# Trouver .text et enccode
text_offset = None
text_size = None
enccode_offset = None
enccode_size = None

for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_name = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_file_offset = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    
    name_start = shstrtab_offset + sh_name
    name_end = name_start
    while name_end < len(data) and data[name_end] != 0:
        name_end += 1
    name = data[name_start:name_end].decode('utf-8', errors='replace')
    
    if name == '.text':
        text_offset = sh_file_offset
        text_size = sh_size
    elif name == 'enccode':
        enccode_offset = sh_file_offset
        enccode_size = sh_size

print(f".text: offset={hex(text_offset)}, size={text_size}")
print(f"enccode: offset={hex(enccode_offset)}, size={enccode_size}")

# Extraire les derniers 200 bytes de .text (la routine de décryptage devrait être là)
text_data = data[text_offset:text_offset+text_size]
print(f"\nDerniers 200 bytes de .text:")
print(text_data[-200:].hex())

# Extraire enccode
enc_data = data[enccode_offset:enccode_offset+enccode_size]
print(f"\nPremiers 50 bytes de enccode (chiffré):")
print(enc_data[:50].hex())
