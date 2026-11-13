# D'abord, vérifions la structure du WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du WAL: {len(data)} octets")
print(f"Header (32 octets): {data[:32].hex()}")

# Magic
import struct
magic = struct.unpack('>I', data[0:4])[0]
print(f"Magic: 0x{magic:08x}")

page_size = struct.unpack('>I', data[8:12])[0]
print(f"Page size: {page_size}")

# Nombre de frames
frame_size = 24 + page_size
num_frames = (len(data) - 32) // frame_size
print(f"Nombre de frames: {num_frames}")