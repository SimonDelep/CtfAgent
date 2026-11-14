import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille totale: {len(data)} octets")

# Header WAL: 32 octets
# Magic: 4 octets (0x377f0682 pour WAL)
# Format version: 4 octets
# Page size: 4 octets
# Checkpoint sequence: 4 octets
# Salt-1: 4 octets
# Salt-2: 4 octets
# Checksum-1: 4 octets
# Checksum-2: 4 octets

if len(data) >= 32:
    magic = struct.unpack('>I', data[0:4])[0]
    print(f"Magic: 0x{magic:08x}")
    
    page_size = struct.unpack('>I', data[8:12])[0]
    print(f"Page size: {page_size}")
    
    # Après le header, chaque frame a:
    # - Page number: 4 octets
    # - Commit flag: 4 octets (si présent)
    # - Données de la page (page_size octets)
    
    # Taille d'une frame = 8 (header frame) + page_size
    frame_header_size = 8
    frame_size = frame_header_size + page_size
    
    num_frames = (len(data) - 32) // frame_size
    print(f"Nombre de frames: {num_frames}")
    print(f"Taille attendue: {32 + num_frames * frame_size}, réelle: {len(data)}")
    
    # Analyser chaque frame
    offset = 32
    for i in range(num_frames):
        frame_start = offset + i * frame_size
        page_num = struct.unpack('>I', data[frame_start:frame_start+4])[0]
        commit_flag = struct.unpack('>I', data[frame_start+4:frame_start+8])[0]
        
        # Chercher des BLOBs de 32 octets dans cette frame
        page_data = data[frame_start+8:frame_start+8+page_size]
        
        # Chercher l'offset 991 (si page_size >= 1024)
        if page_size >= 1024:
            candidate = page_data[991:991+32]
            # Vérifier si c'est un candidat valide (pas trop de null bytes)
            if candidate.count(b'\x00') < 20:  # seuil arbitraire
                print(f"Frame {i}: page={page_num}, commit={commit_flag}, offset991={candidate.hex()}")