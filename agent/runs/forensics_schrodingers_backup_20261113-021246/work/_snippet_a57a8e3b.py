import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

# Cherchons des séquences de 32 octets qui pourraient être north ou south
# Les valeurs north et south sont des BLOB de 32 octets

# D'abord, regardons la structure des pages dans le WAL
page_size = 1024
frame_header_size = 24
header_size = 32

# Analysons chaque frame pour trouver des données intéressantes
for i in range(39):  # 39 frames
    frame_start = header_size + i * frame_header_size
    page_data = data[frame_start + frame_header_size:frame_start + frame_header_size + page_size]
    
    # Cherchons des séquences de 32 octets non nulles
    # Les valeurs north/south sont des BLOB de 32 octets
    
    # Cherchons le motif 0d00000001 qui semble être un en-tête d'enregistrement
    pos = 0
    while True:
        pos = page_data.find(b'\x0d\x00\x00\x00\x01', pos)
        if pos == -1:
            break
        
        # Après ce motif, il y a 03XX0003YY
        if pos + 13 <= len(page_data):
            # Regardons ce qui suit
            after = page_data[pos:pos+50]
            print(f"Frame {i+1}, offset {pos}: {after.hex()}")
            
            # Extraire les valeurs
            # Le motif est: 0d 00 00 00 01 03 XX 00 03 YY
            # Peut-être que XX et YY sont des références à des pages ou des IDs
            val1 = struct.unpack('>H', page_data[pos+5:pos+7])[0]
            val2 = struct.unpack('>H', page_data[pos+9:pos+11])[0]
            print(f"  Valeurs: {val1} (0x{val1:04x}), {val2} (0x{val2:04x})")
        
        pos += 1
