import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)} octets")

# Header WAL: 32 octets
# Magic: 4 octets (0x377f0682 ou 0x377f0683)
# Format version: 4 octets
# Page size: 4 octets
# Checkpoint sequence: 4 octets
# Salt-1: 4 octets
# Salt-2: 4 octets
# Checksum-1: 4 octets
# Checksum-2: 4 octets

header = data[:32]
magic = struct.unpack('>I', header[0:4])[0]
print(f"Magic: 0x{magic:08x}")
version = struct.unpack('>I', header[4:8])[0]
print(f"Version: {version}")
page_size = struct.unpack('>I', header[8:12])[0]
print(f"Page size: {page_size}")
checkpoint_seq = struct.unpack('>I', header[12:16])[0]
print(f"Checkpoint sequence: {checkpoint_seq}")
salt1 = struct.unpack('>I', header[16:20])[0]
salt2 = struct.unpack('>I', header[20:24])[0]
print(f"Salt1: 0x{salt1:08x}, Salt2: 0x{salt2:08x}")

# Chaque frame est de (page_size + 24) octets
# 24 octets de header de frame
frame_size = page_size + 24
print(f"Frame size: {frame_size}")

# Nombre de frames
num_frames = (len(data) - 32) // frame_size
print(f"Nombre de frames: {num_frames}")

# Analyser chaque frame
for i in range(min(5, num_frames)):
    frame_start = 32 + i * frame_size
    frame_header = data[frame_start:frame_start+24]
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    print(f"\nFrame {i}: page_num={page_num}, commit_flag={commit_flag}")
    
    # Page data
    page_data = data[frame_start+24:frame_start+24+page_size]
    # Premier octet est le type de page
    page_type = page_data[0]
    print(f"  Page type: 0x{page_type:02x}")
    
    if page_type == 0x0d:  # Leaf table b-tree page
        print(f"  C'est une page de feuille de table!")
        # Afficher un peu de contenu
        print(f"  Contenu (hex): {page_data[:64].hex()}")