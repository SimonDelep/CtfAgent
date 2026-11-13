import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du WAL: {len(data)} octets")

# Header WAL: 32 octets
# - Magic number (4 bytes): 0x377f0682 ou 0x377f0683
# - File format version (4 bytes)
# - Page size (4 bytes)
# - Checkpoint sequence number (4 bytes)
# - Salt-1 (4 bytes)
# - Salt-2 (4 bytes)
# - Checksum-1 (4 bytes)
# - Checksum-2 (4 bytes)

header = data[:32]
magic = struct.unpack('>I', header[0:4])[0]
print(f"Magic: 0x{magic:08x}")
page_size = struct.unpack('>I', header[4:8])[0]
print(f"Page size: {page_size}")
checkpoint_seq = struct.unpack('>I', header[8:12])[0]
print(f"Checkpoint sequence: {checkpoint_seq}")

# Chaque frame est de taille (page_size + 24)
# 24 octets d'en-tête de frame
frame_size = page_size + 24
print(f"Frame size: {frame_size}")

num_frames = len(data) // frame_size
print(f"Nombre de frames: {num_frames}")

# Analyser chaque frame
for i in range(min(5, num_frames)):
    offset = 32 + i * frame_size
    frame_header = data[offset:offset+24]
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    print(f"\nFrame {i}: page={page_num}, commit={commit_flag}")
    
    # Le contenu de la page commence après l'en-tête de frame
    page_data = data[offset+24:offset+24+page_size]
    
    # Chercher des séquences non nulles de 32 octets
    for j in range(len(page_data) - 32):
        chunk = page_data[j:j+32]
        if chunk.count(b'\x00') < 20:  # Pas trop de zéros
            print(f"  Offset {j}: {chunk.hex()}")