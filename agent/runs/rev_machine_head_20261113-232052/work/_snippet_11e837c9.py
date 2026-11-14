import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)}")

# Les segments LOAD:
# LOAD 0: offset=0x0, vaddr=0x0, filesz=0x750 → 0x0 à 0x750
# LOAD 1: offset=0x1000, vaddr=0x1000, filesz=0x329 → 0x1000 à 0x1329
# LOAD 2: offset=0x2000, vaddr=0x2000, filesz=0x8a0 → 0x2000 à 0x28a0
# LOAD 3: offset=0x2da0, vaddr=0x3da0, filesz=0x270 → 0x2da0 à 0x3010

# Donc pour une adresse virtuelle vaddr:
# - Si vaddr < 0x750: offset = vaddr
# - Si 0x1000 <= vaddr < 0x1329: offset = vaddr
# - Si 0x2000 <= vaddr < 0x28a0: offset = vaddr
# - Si 0x3da0 <= vaddr < 0x4010: offset = 0x2da0 + (vaddr - 0x3da0)

# Les adresses que nous cherchons:
# 0x4000 est dans le segment 3: offset = 0x2da0 + (0x4000 - 0x3da0) = 0x2da0 + 0x260 = 0x3000

def vaddr_to_offset(vaddr):
    if vaddr < 0x750:
        return vaddr
    elif 0x1000 <= vaddr < 0x1329:
        return vaddr
    elif 0x2000 <= vaddr < 0x28a0:
        return vaddr
    elif 0x3da0 <= vaddr < 0x4010:
        return 0x2da0 + (vaddr - 0x3da0)
    else:
        return None

def read_qword(vaddr):
    offset = vaddr_to_offset(vaddr)
    if offset is None:
        return None
    if offset + 8 > len(data):
        return None
    return struct.unpack('<Q', data[offset:offset+8])[0]

def read_byte(vaddr):
    offset = vaddr_to_offset(vaddr)
    if offset is None:
        return None
    if offset >= len(data):
        return None
    return data[offset]

# Adresses à lire:
# [rip + 0x2d66] à 0x1273: rip après = 0x127a, addr = 0x127a + 0x2d66 = 0x3fe0
# [rip + 0x2d35] à 0x12b4: rip après = 0x12bb, addr = 0x12bb + 0x2d35 = 0x3ff0
# [rip + 0x2d12] à 0x12de: rip après = 0x12e6, addr = 0x12e6 + 0x2d12 = 0x3ff8
# [rip + 0x2d16] à 0x12eb: rip après = 0x12f2, addr = 0x12f2 + 0x2d16 = 0x4008
# [rip + 0x2d4d] à 0x12d4: rip après = 0x12db, addr = 0x12db + 0x2d4d = 0x4028
# [rip + 0x2da9] à 0x1260: rip après = 0x1267, addr = 0x1267 + 0x2da9 = 0x4010
# [rip + 0x2da2] à 0x1267: rip après = 0x126e, addr = 0x126e + 0x2da2 = 0x4010
# [rip + 0x2d79] à 0x1290: rip après = 0x1297, addr = 0x1297 + 0x2d79 = 0x4010
# [rip + 0x2d72] à 0x1297: rip après = 0x129e, addr = 0x129e + 0x2d72 = 0x4010

print("Valeurs aux adresses:")
print(f"0x3fe0: {read_qword(0x3fe0)}")
print(f"0x3ff0: {read_qword(0x3ff0)}")
print(f"0x3ff8: {read_qword(0x3ff8)}")
print(f"0x4008: {read_qword(0x4008)}")
print(f"0x4010: {read_qword(0x4010)}")
print(f"0x4028: {read_byte(0x4028)}")

# Regardons les données autour de 0x4010
print("\nDonnées à partir de 0x4010:")
for i in range(0, 100, 16):
    addr = 0x4010 + i
    offset = vaddr_to_offset(addr)
    if offset and offset + 16 <= len(data):
        hex_data = ' '.join(f'{b:02x}' for b in data[offset:offset+16])
        print(f"0x{addr:04x} (offset {offset:#x}): {hex_data}")