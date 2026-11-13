# Analysons le fichier WAL pour comprendre sa structure
# SQLite WAL format: header (32 bytes) + frames (24 bytes header + page data)

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du WAL: {len(data)} bytes")

# Header WAL (32 bytes)
header = data[:32]
print(f"\nHeader WAL (hex): {header.hex()}")

# Magic number (should be 0x377f0682 or 0x377f0683)
magic = int.from_bytes(header[:4], 'big')
print(f"Magic: 0x{magic:08x}")

# Format version
version = int.from_bytes(header[4:8], 'big')
print(f"Version: {version}")

# Page size
page_size = int.from_bytes(header[8:12], 'big')
print(f"Page size: {page_size}")

# Checkpoint sequence number
ckpt_seq = int.from_bytes(header[12:16], 'big')
print(f"Checkpoint sequence: {ckpt_seq}")

# Number of frames in header
print(f"Header rest: {header[16:].hex()}")

# Chaque frame a un header de 24 bytes suivi de page_size bytes de données
frame_header_size = 24
offset = 32  # après le header WAL

frame_num = 0
while offset < len(data):
    if offset + frame_header_size > len(data):
        print(f"Frame {frame_num}: header incomplet à offset {offset}")
        break
    
    frame_header = data[offset:offset+frame_header_size]
    page_num = int.from_bytes(frame_header[:4], 'big')
    commit_flag = int.from_bytes(frame_header[4:8], 'big')
    db_size_pages = int.from_bytes(frame_header[8:12], 'big')
    salt1 = int.from_bytes(frame_header[12:16], 'big')
    salt2 = int.from_bytes(frame_header[16:20], 'big')
    checksum1 = int.from_bytes(frame_header[20:24], 'big')
    
    print(f"\nFrame {frame_num}:")
    print(f"  Page num: {page_num}")
    print(f"  Commit flag: {commit_flag}")
    print(f"  DB size pages: {db_size_pages}")
    print(f"  Salt: {salt1}, {salt2}")
    
    page_data_offset = offset + frame_header_size
    page_data = data[page_data_offset:page_data_offset+page_size]
    
    # Afficher les premières données de la page
    print(f"  Page data (first 64 bytes): {page_data[:64].hex()}")
    
    offset = page_data_offset + page_size
    frame_num += 1
    
    if frame_num > 20:  # limite de sécurité
        print("... (limité à 20 frames)")
        break

print(f"\nTotal frames trouvées: {frame_num}")