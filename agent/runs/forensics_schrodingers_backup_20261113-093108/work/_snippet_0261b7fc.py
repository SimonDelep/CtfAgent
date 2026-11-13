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

# Les blobs de 35 octets ont un header de 3 octets. Regardons si le troisième octet varie
print("Analyse des headers des blobs:")
for tx_idx, tx in enumerate(transactions):
    for rowid, payload in tx:
        if len(payload) == 35:
            header = payload[:3]
            data_bytes = payload[3:]
            print(f"TX {tx_idx+1}: header={header.hex()}, third_byte={header[2]:02x} ({header[2]})")