import struct

def read_varint(data, offset):
    """Lire un varint SQLite"""
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

def parse_page_leaf(data, page_num):
    """Parser une page table leaf et extraire les BLOBs"""
    results = []
    
    # Header de page: 8 octets minimum
    if len(data) < 8:
        return results
    
    page_type = data[0]
    if page_type != 0x0d:
        return results
    
    # Header: type(1), freeblock(2), cell_count(2), cell_content_start(2), fragmented(1)
    cell_count = struct.unpack(">H", data[3:5])[0]
    
    # Pointeurs de cellules commencent à offset 8
    cell_pointers_offset = 8
    
    for i in range(cell_count):
        ptr_offset = cell_pointers_offset + i * 2
        if ptr_offset + 2 > len(data):
            break
        cell_offset = struct.unpack(">H", data[ptr_offset:ptr_offset+2])[0]
        
        if cell_offset >= len(data):
            continue
        
        # Parser la cellule
        offset = cell_offset
        
        # payload_length (varint)
        payload_len, offset = read_varint(data, offset)
        
        # rowid (varint)
        rowid, offset = read_varint(data, offset)
        
        # payload
        payload = data[offset:offset+payload_len]
        
        results.append({
            'page': page_num,
            'cell': i,
            'rowid': rowid,
            'payload_len': payload_len,
            'payload': payload
        })
    
    return results

# Lire le WAL
with open("catalog.db-wal", "rb") as f:
    wal_data = f.read()

page_size = struct.unpack(">I", wal_data[8:12])[0]
frame_header_size = 24

offset = 32
frame_num = 0
all_blobs = []

while offset + frame_header_size + page_size <= len(wal_data):
    page_data = wal_data[offset+frame_header_size:offset+frame_header_size+page_size]
    page_type = page_data[0]
    
    if page_type == 0x0d:
        cells = parse_page_leaf(page_data, frame_num)
        for cell in cells:
            payload = cell['payload']
            # Chercher des BLOBs de 32 octets
            if cell['payload_len'] == 32:
                all_blobs.append(cell)
                print(f"Frame {frame_num}, cell {cell['cell']}, rowid {cell['rowid']}: {payload.hex()}")
    
    offset += frame_header_size + page_size
    frame_num += 1

print(f"\nTotal BLOBs de 32 octets trouvés: {len(all_blobs)}")