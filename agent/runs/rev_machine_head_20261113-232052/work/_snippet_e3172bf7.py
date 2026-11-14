import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Les adresses virtuelles sont relatives au segment LOAD à vaddr=0x1000, offset=0x1000
# Donc pour convertir une adresse virtuelle en offset fichier: offset = addr - 0x1000 + 0x1000 = addr

# Regardons les valeurs à certaines adresses
# [rip + 0x2d66] à l'adresse 0x1273: rip après l'instruction est 0x127a
# Donc adresse = 0x127a + 0x2d66 = 0x3fe0

# [rip + 0x2d35] à l'adresse 0x12b4: rip après l'instruction est 0x12bb
# Donc adresse = 0x12bb + 0x2d35 = 0x3ff0

# [rip + 0x2d12] à l'adresse 0x12de: rip après l'instruction est 0x12e6
# Donc adresse = 0x12e6 + 0x2d12 = 0x3ff8

# [rip + 0x2d16] à l'adresse 0x12eb: rip après l'instruction est 0x12f2
# Donc adresse = 0x12f2 + 0x2d16 = 0x4008

# [rip + 0x2d4d] à l'adresse 0x12d4: rip après l'instruction est 0x12db
# Donc adresse = 0x12db + 0x2d4d = 0x4028

# [rip + 0x2da9] à l'adresse 0x1260: rip après l'instruction est 0x1267
# Donc adresse = 0x1267 + 0x2da9 = 0x4010

# [rip + 0x2da2] à l'adresse 0x1267: rip après l'instruction est 0x126e
# Donc adresse = 0x126e + 0x2da2 = 0x4010

# [rip + 0x2d79] à l'adresse 0x1290: rip après l'instruction est 0x1297
# Donc adresse = 0x1297 + 0x2d79 = 0x4010

# [rip + 0x2d72] à l'adresse 0x1297: rip après l'instruction est 0x129e
# Donc adresse = 0x129e + 0x2d72 = 0x4010

# Lisons ces adresses
def read_qword(addr):
    return struct.unpack('<Q', data[addr:addr+8])[0]

def read_byte(addr):
    return data[addr]

print("Adresses à lire (offset fichier = adresse virtuelle):")
print(f"0x4000: {read_qword(0x4000):#x}")
print(f"0x4008: {read_qword(0x4008):#x}")
print(f"0x4010: {read_qword(0x4010):#x}")
print(f"0x4018: {read_qword(0x4018):#x}")
print(f"0x4020: {read_qword(0x4020):#x}")
print(f"0x4028: {read_qword(0x4028):#x}")
print(f"0x4030: {read_qword(0x4030):#x}")

# Regardons aussi les données autour de 0x4000
print("\nDonnées hex à partir de 0x4000:")
for i in range(0, 200, 16):
    addr = 0x4000 + i
    hex_data = ' '.join(f'{b:02x}' for b in data[addr:addr+16])
    print(f"0x{addr:04x}: {hex_data}")