import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du WAL: {len(data)} octets")

# Header WAL: 32 octets
# Magic number (4 octets): 0x377f0682 ou 0x377f0683
magic = struct.unpack('>I', data[0:4])[0]
print(f"Magic: {hex(magic)}")

# Page size (4 octets, offset 8)
page_size = struct.unpack('>I', data[8:12])[0]
print(f"Page size: {page_size}")

# Nombre de frames
# Chaque frame = 24 octets header + page_size octets données
frame_header_size = 24
frame_size = frame_header_size + page_size

# Header WAL = 32 octets
header_size = 32

# Nombre de frames
num_frames = (len(data) - header_size) // frame_size
print(f"Nombre de frames estimées: {num_frames}")

# Vérifions la taille attendue
expected_size = header_size + num_frames * frame_size
print(f"Taille attendue: {expected_size}, Taille réelle: {len(data)}")