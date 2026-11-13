import struct

def read_varint(data, offset):
    """Lit un varint SQLite et retourne (valeur, nouveau_offset)"""
    result = 0
    for i in range(9):
        if offset + i >= len(data):
            break
        byte = data[offset + i]
        if i < 8:
            result = (result << 7) | (byte & 0x7f)
            if byte < 0x80:
                return result, offset + i + 1
        else:
            result = (result << 8) | byte
            return result, offset + i + 1
    return result, offset

def parse_page_leaf(page_data):
    """Parse une page de type table leaf et retourne les cellules"""
    if page_data[0] != 0x0d:
        return []
    
    # Nombre de cellules (bytes 3-4)
    num_cells = struct.unpack('>H', page_data[3:5])[0]
    
    # Début des pointeurs de cellules (bytes 8+)
    cell_pointers_start = 8
    
    cells = []
    for i in range(num_cells):
        ptr_offset = cell_pointers_start + i * 2
        if ptr_offset + 2 > len(page_data):
            break
        cell_offset = struct.unpack('>H', page_data[ptr_offset:ptr_offset + 2])[0]
        
        if cell_offset < len(page_data):
            # Lire la cellule
            offset = cell_offset
            
            # Taille de la charge utile (varint)
            payload_size, offset = read_varint(page_data, offset)
            
            # RowID (varint)
            rowid, offset = read_varint(page_data, offset)
            
            # Charge utile
            payload = page_data[offset:offset + payload_size]
            
            cells.append({
                'rowid': rowid,
                'payload': payload,
                'payload_hex': payload.hex()
            })
    
    return cells

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

header_size = 32
frame_header_size = 24
page_size = 1024

num_frames = (len(data) - header_size) // (frame_header_size + page_size)

print(f"Analyse de {num_frames} frames...\n")

all_cells = []

for i in range(num_frames):
    frame_offset = header_size + i * (frame_header_size + page_size)
    frame_header = data[frame_offset:frame_offset + frame_header_size]
    
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    
    page_data = data[frame_offset + frame_header_size:frame_offset + frame_header_size + page_size]
    
    cells = parse_page_leaf(page_data)
    
    if cells:
        print(f"Frame {i}, page {page_num}, commit={commit_flag}: {len(cells)} cellules")
        for cell in cells:
            print(f"  rowid={cell['rowid']}, payload={cell['payload_hex']}")
            all_cells.append({
                'frame': i,
                'page': page_num,
                'commit': commit_flag,
                'rowid': cell['rowid'],
                'payload': cell['payload']
            })

print(f"\nTotal: {len(all_cells)} cellules trouvées")
