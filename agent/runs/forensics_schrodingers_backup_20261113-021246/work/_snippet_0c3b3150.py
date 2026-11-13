import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024
frame_header_size = 24
frame_size = page_size + frame_header_size

# Header WAL: 32 octets
header_size = 32

num_frames = (len(data) - header_size) // frame_size
print(f"Nombre de frames: {num_frames}")

# Analyser chaque frame
for i in range(num_frames):
    offset = header_size + i * frame_size
    frame_header = data[offset:offset+frame_header_size]
    
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    
    # Le contenu de la page
    page_data = data[offset+frame_header_size:offset+frame_header_size+page_size]
    
    print(f"\nFrame {i}: page={page_num}, commit={commit_flag}")
    
    # Chercher des séquences de 32 octets non nulles
    # Les blobs de 32 octets devraient être des valeurs north/south
    for j in range(len(page_data) - 31):
        chunk = page_data[j:j+32]
        # Si le chunk a peu de zéros, c'est potentiellement un blob
        non_zero = sum(1 for b in chunk if b != 0)
        if non_zero >= 24:  # Au moins 24 octets non nuls
            print(f"  Offset {j} (non_zero={non_zero}): {chunk.hex()}")