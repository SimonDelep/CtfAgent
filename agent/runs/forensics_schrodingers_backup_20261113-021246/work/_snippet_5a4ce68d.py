import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

# Le header WAL est de 32 octets
# Ensuite viennent les frames
# Chaque frame a:
# - 24 octets de header de frame
# - page_size octets de données de page

page_size = 1024
frame_header_size = 24

# Header WAL (32 octets)
print("=== Header WAL ===")
print(f"Magic: {data[0:4].hex()}")
print(f"Version: {struct.unpack('>I', data[4:8])[0]}")
print(f"Page size: {struct.unpack('>I', data[8:12])[0]}")
print(f"Checkpoint sequence: {struct.unpack('>I', data[12:16])[0]}")
print(f"Salt 1: {struct.unpack('>I', data[16:20])[0]}")
print(f"Salt 2: {struct.unpack('>I', data[20:24])[0]}")
print(f"Checksum 1: {struct.unpack('>I', data[24:28])[0]}")
print(f"Checksum 2: {struct.unpack('>I', data[28:32])[0]}")

# Calculons le nombre de frames
# Taille totale = 32 (header) + n * (24 + page_size)
total_size = len(data)
header_size = 32
frame_size = frame_header_size + page_size
num_frames = (total_size - header_size) // frame_size
print(f"\nNombre de frames: {num_frames}")

# Analysons chaque frame
for i in range(min(10, num_frames)):
    frame_start = header_size + i * frame_size
    frame_header = data[frame_start:frame_start + frame_header_size]
    page_data = data[frame_start + frame_header_size:frame_start + frame_header_size + page_size]
    
    # Header de frame:
    # - 4 octets: numéro de page
    # - 4 octets: taille de la transaction (ou 0 si dernière frame)
    # - 8 octets: salt
    # - 8 octets: checksum
    
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    tx_size = struct.unpack('>I', frame_header[4:8])[0]
    
    print(f"\n=== Frame {i+1}: page {page_num}, tx_size={tx_size} ===")
    
    # Cherchons "CSAW" dans la page
    if b'CSAW' in page_data:
        idx = page_data.find(b'CSAW')
        print(f"  CSAW trouvé à offset {idx} dans la page")
        # Affichons le contexte
        start = max(0, idx - 10)
        end = min(len(page_data), idx + 100)
        print(f"  Contexte: {page_data[start:end].hex()}")
        
        # Cherchons le motif 0d00000001
        if b'\x0d\x00\x00\x00\x01' in page_data:
            pos = page_data.find(b'\x0d\x00\x00\x00\x01')
            print(f"  Motif 0d00000001 à offset {pos}")
            # Après ce motif, il y a 03XX0003XX
            if pos + 13 < len(page_data):
                motif = page_data[pos:pos+13]
                print(f"  Données: {motif.hex()}")
                # Extraire les valeurs
                # 0d00000001 03XX00 03YY
                # Peut-être que 03XX et 03YY sont des références
                val1 = struct.unpack('>H', page_data[pos+5:pos+7])[0]
                val2 = struct.unpack('>H', page_data[pos+9:pos+11])[0]
                print(f"  Valeurs: {val1} (0x{val1:04x}), {val2} (0x{val2:04x})")
