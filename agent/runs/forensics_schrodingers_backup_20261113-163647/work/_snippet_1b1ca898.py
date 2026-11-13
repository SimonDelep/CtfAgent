import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

# Header WAL: 32 bytes
# Magic: 4 bytes (0x377f0682)
# Format version: 4 bytes
# Page size: 4 bytes
# Checkpoint sequence: 4 bytes
# Salt-1: 4 bytes
# Salt-2: 4 bytes
# Checksum-1: 4 bytes
# Checksum-2: 4 bytes

header = data[:32]
magic = struct.unpack('>I', header[0:4])[0]
page_size = struct.unpack('>I', header[8:12])[0]
checkpoint_seq = struct.unpack('>I', header[12:16])[0]

print(f"Magic: 0x{magic:08x}")
print(f"Page size: {page_size}")
print(f"Checkpoint sequence: {checkpoint_seq}")

# Chaque frame: 24 bytes header + page_size bytes de données
# Frame header: 8 bytes (page number, commit flag, etc.) + 16 bytes de checksums/salt

# Calculer le nombre de frames
frame_header_size = 24
total_frames = (len(data) - 32) // (frame_header_size + page_size)
print(f"Total frames: {total_frames}")

# Parcourir chaque frame
offset = 32
for i in range(total_frames):
    frame_header = data[offset:offset+frame_header_size]
    page_data = data[offset+frame_header_size:offset+frame_header_size+page_size]
    
    # Frame header: 4 bytes page number, 4 bytes commit flag (0 si pas de commit, taille de page si commit)
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    
    is_commit = (commit_flag == page_size)
    
    # Vérifier si c'est une page de type table leaf (0x0d)
    if len(page_data) > 0 and page_data[0] == 0x0d:
        print(f"Frame {i}: page_num={page_num}, commit_flag={commit_flag}, is_commit={is_commit}")
        # Afficher les premières données
        print(f"  Page data (first 100 bytes): {page_data[:100].hex()}")
    
    offset += frame_header_size + page_size