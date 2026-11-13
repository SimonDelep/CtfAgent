import struct

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Vérifier l'entête ELF
print("Magic:", data[:4])
print("Class:", data[4])  # 1=32bit, 2=64bit
print("Endian:", data[5])  # 1=little, 2=big
print("Arch:", data[6])  # 0=x86, 3=ARM, etc.

# Parser l'entête ELF 64-bit
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

print(f"Type: {e_type}, Machine: {e_machine:#x}")
print(f"Entry: {e_entry:#x}")
print(f"PHoff: {e_phoff:#x}, SHoff: {e_shoff:#x}")
print(f"PHnum: {e_phnum}, SHnum: {e_shnum}, SHstrndx: {e_shstrndx}")

# Machine x86-64 = 0x3E (62)
print(f"Expected x86-64 machine: 0x3E")