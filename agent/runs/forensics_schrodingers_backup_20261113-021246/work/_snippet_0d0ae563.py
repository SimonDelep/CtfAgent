import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du WAL: {len(data)} octets")

# Header WAL: 32 octets
header = data[:32]
print("Header hex:", header.hex())

# Le format WAL peut être big-endian ou little-endian selon le magic
# 0x377f0682 = big-endian, 0x82067f37 = little-endian
magic_be = struct.unpack('>I', header[0:4])[0]
magic_le = struct.unpack('<I', header[0:4])[0]
print(f"Magic BE: 0x{magic_be:08x}")
print(f"Magic LE: 0x{magic_le:08x}")

# Pour SQLite WAL, le format est big-endian
# Header:
# [0:4]   Magic (0x377f0682 ou 0x377f0683)
# [4:8]   File format version (3007000 = 0x2d108c pour version 3007000)
# [8:12]  Page size
# [12:16] Checkpoint sequence number
# [16:20] Salt-1
# [20:24] Salt-2
# [24:28] Checksum-1
# [28:32] Checksum-2

# Attends, regardons les bytes
print("\nBytes 0-3 (magic):", header[0:4].hex())
print("Bytes 4-7 (version):", header[4:8].hex())
print("Bytes 8-11 (page_size):", header[8:12].hex())
print("Bytes 12-15 (checkpoint_seq):", header[12:16].hex())

# Essayons de décoder page_size en big-endian
page_size = struct.unpack('>I', header[8:12])[0]
print(f"Page size (BE): {page_size}")

# Peut-être que c'est little-endian?
page_size_le = struct.unpack('<I', header[8:12])[0]
print(f"Page size (LE): {page_size_le}")

# Regardons aussi les bytes 4-7
version_be = struct.unpack('>I', header[4:8])[0]
version_le = struct.unpack('<I', header[4:8])[0]
print(f"Version BE: {version_be}")
print(f"Version LE: {version_le}")