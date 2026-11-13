import struct

def extract_wal_data(wal_path):
    with open(wal_path, 'rb') as f:
        data = f.read()
    
    page_size = struct.unpack('>I', data[8:12])[0]
    frame_header_size = 24
    offset = 32
    
    transactions = []
    current_tx = []
    
    while offset + frame_header_size <= len(data):
        frame_header = data[offset:offset+frame_header_size]
        page_number = struct.unpack('>I', frame_header[0:4])[0]
        commit_flag = struct.unpack('>I', frame_header[4:8])[0]
        
        page_data = data[offset+frame_header_size:offset+frame_header_size+page_size]
        
        if len(page_data) > 0 and page_data[0] == 0x0d:
            cell_count = struct.unpack('>H', page_data[3:5])[0]
            cell_pointers_offset = 8
            
            for i in range(cell_count):
                ptr_offset = cell_pointers_offset + i * 2
                if ptr_offset + 2 <= len(page_data):
                    cell_ptr = struct.unpack('>H', page_data[ptr_offset:ptr_offset+2])[0]
                    if cell_ptr < len(page_data):
                        pos = cell_ptr
                        payload_size = 0
                        shift = 0
                        while True:
                            if pos >= len(page_data):
                                break
                            b = page_data[pos]
                            pos += 1
                            payload_size |= (b & 0x7f) << shift
                            if b < 0x80:
                                break
                            shift += 7
                        
                        rowid = 0
                        shift = 0
                        while True:
                            if pos >= len(page_data):
                                break
                            b = page_data[pos]
                            pos += 1
                            rowid |= (b & 0x7f) << shift
                            if b < 0x80:
                                break
                            shift += 7
                        
                        payload = page_data[pos:pos+payload_size]
                        current_tx.append((rowid, payload))
        
        offset += frame_header_size + page_size
        
        if commit_flag != 0:
            if current_tx:
                transactions.append(current_tx)
            current_tx = []
    
    return transactions

transactions = extract_wal_data('catalog.db-wal')

# Collecter tous les blobs de 35 octets (qui contiennent 32 octets de données après le header)
all_blobs = []
for tx_idx, tx in enumerate(transactions):
    for rowid, payload in tx:
        if len(payload) == 35:
            # Le header de cellule est probablement 3 octets (type + taille + rowid varint)
            # Les 32 octets suivants sont les données
            # Regardons la structure: 03 00 XX ... où XX est peut-être le type
            # En fait, le payload_size est 35, donc tout le payload est de 35 octets
            # Le header de cellule (dans la page) contient déjà payload_size et rowid
            # Donc le payload lui-même est de 35 octets
            # Décomposons: probablement 3 octets de header + 32 octets de données
            header = payload[:3]
            data_bytes = payload[3:]
            if len(data_bytes) == 32:
                all_blobs.append((tx_idx, rowid, data_bytes))

print(f"Nombre de blobs de 32 octets trouvés: {len(all_blobs)}")
for tx_idx, rowid, data_bytes in all_blobs:
    print(f"Transaction {tx_idx+1}, rowid={rowid}: {data_bytes.hex()}")