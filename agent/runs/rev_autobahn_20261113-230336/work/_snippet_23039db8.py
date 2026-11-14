import struct

with open('nitro', 'rb') as f:
    data = f.read()

# Offset de 0x401306
def vaddr_to_offset(vaddr):
    e_phoff = 0x40
    e_phentsize = 0x38
    e_phnum = 13
    for i in range(e_phnum):
        ph_offset = e_phoff + i * e_phentsize
        p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
        if p_type == 1:
            p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
            p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
            p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
            if p_vaddr <= vaddr < p_vaddr + p_filesz:
                return p_offset + (vaddr - p_vaddr)
    return None

# 0x401306 est dans le segment LOAD
offset_401306 = vaddr_to_offset(0x401306)
offset_40130d = vaddr_to_offset(0x40130d)
offset_4020a1 = vaddr_to_offset(0x4020a1)
offset_4020a8 = vaddr_to_offset(0x4020a8)

print(f"0x401306 -> offset 0x{offset_401306:x}")
print(f"0x40130d -> offset 0x{offset_40130d:x}")
print(f"0x4020a1 -> offset 0x{offset_4020a1:x}")
print(f"0x4020a8 -> offset 0x{offset_4020a8:x}")

# Lire les données
print("\nDonnées à 0x401306 (offset 0x%x):" % offset_401306)
print(data[offset_401306:offset_401306+20].hex())

print("\nDonnées à 0x40130d (offset 0x%x):" % offset_40130d)
print(data[offset_40130d:offset_40130d+20].hex())

print("\nDonnées à 0x4020a1 (offset 0x%x):" % offset_4020a1)
print(data[offset_4020a1:offset_4020a1+20].hex())

print("\nDonnées à 0x4020a8 (offset 0x%x):" % offset_4020a8)
print(data[offset_4020a8:offset_4020a8+20].hex())