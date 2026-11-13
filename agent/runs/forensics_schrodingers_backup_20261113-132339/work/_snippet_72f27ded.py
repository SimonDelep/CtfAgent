import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille totale: {len(data)} octets")

# Header WAL : 32 octets
# Magic: 4 octets (0x377f0682 ou 0x377f0683)
# Format version: 4 octets
# Page size: 4 octets
# Checkpoint seq: 4 octets
# Salt-1: 4 octets
# Salt-2: 4 octets
# Checksum-1: 4 octets
# Checksum-2: 4 octets

magic = struct.unpack('>I', data[0:4])[0]
print(f"Magic: 0x{magic:08x}")

page_size = struct.unpack('>I', data[8:12])[0]
print(f"Page size: {page_size}")

checkpoint_seq = struct.unpack('>I', data[12:16])[0]
print(f"Checkpoint seq: {checkpoint_seq}")

salt1 = struct.unpack('>I', data[16:20])[0]
salt2 = struct.unpack('>I', data[20:24])[0]
print(f"Salt1: 0x{salt1:08x}, Salt2: 0x{salt2:08x}")

# Nombre de frames
# Chaque frame = header_frame (24 octets) + page_data (page_size octets)
header_size = 32
frame_header_size = 24

remaining = len(data) - header_size
num_frames = remaining // (frame_header_size + page_size)
print(f"Nombre de frames estimées: {num_frames}")

# Analyser chaque frame
for i in range(min(10, num_frames)):
    frame_offset = header_size + i * (frame_header_size + page_size)
    frame_header = data[frame_offset:frame_offset + frame_header_size]
    
    # Page number dans le fichier DB
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    salt1_frame = struct.unpack('>I', frame_header[8:12])[0]
    salt2_frame = struct.unpack('>I', frame_header[12:16])[0]
    checksum1 = struct.unpack('>I', frame_header[16:20])[0]
    checksum2 = struct.unpack('>I', frame_header[20:24])[0]
    
    page_data = data[frame_offset + frame_header_size:frame_offset + frame_header_size + page_size]
    
    # Type de page : premier octet après le header de page (si c'est une page de données)
    # Pour une page de table leaf (0x0d), le premier octet est 0x0d
    page_type = page_data[0]
    
    print(f"Frame {i}: page_num={page_num}, commit_flag={commit_flag}, page_type=0x{page_type:02x}")
    
    # Chercher des patterns intéressants
    if page_type == 0x0d:  # Table leaf
        print(f"  -> Page de type table leaf")
        # Afficher quelques octets
        print(f"  Données: {page_data[:64].hex()}")
