SCHEMA = {
  "name": "wal_extractor",
  "description": "Extrait les blobs north et south d'un fichier WAL SQLite en analysant les pages de type table leaf (0x0d)",
  "parameters": {
    "properties": {
      "wal_path": {
        "description": "Chemin du fichier WAL",
        "type": "string"
      }
    },
    "required": [
      "wal_path"
    ],
    "type": "object"
  }
}

import struct

def main(args):
    wal_path = args["wal_path"]
    
    with open(wal_path, 'rb') as f:
        data = f.read()
    
    # Header WAL : 32 octets
    # magic (4) + format_version (4) + page_size (4) + checkpoint_seq (4) + salt1 (4) + salt2 (4) + checksum1 (4) + checksum2 (4)
    if len(data) < 32:
        return "Fichier trop petit"
    
    magic = struct.unpack('>I', data[0:4])[0]
    page_size = struct.unpack('>I', data[8:12])[0]
    
    print(f"Magic: 0x{magic:08x}")
    print(f"Page size: {page_size}")
    
    # Les frames commencent après le header (32 octets)
    # Chaque frame : 24 octets header + page_size octets de page
    frame_header_size = 24
    offset = 32
    
    transactions = []
    current_tx = []
    
    while offset + frame_header_size <= len(data):
        # Header de frame : page_number (4) + commit_flag (4) + salt1 (4) + salt2 (4) + checksum1 (4) + checksum2 (4)
        frame_header = data[offset:offset+frame_header_size]
        page_number = struct.unpack('>I', frame_header[0:4])[0]
        commit_flag = struct.unpack('>I', frame_header[4:8])[0]
        
        page_data = data[offset+frame_header_size:offset+frame_header_size+page_size]
        
        # Vérifier si c'est une page de type table leaf (0x0d)
        if len(page_data) > 0 and page_data[0] == 0x0d:
            # C'est une page de table leaf - chercher les cellules
            # Header de page : type (1) + first_freeblock (2) + cell_count (2) + cell_content_start (2) + fragmented_free_bytes (1)
            cell_count = struct.unpack('>H', page_data[3:5])[0]
            
            # Les pointeurs de cellules commencent après le header de page (8 octets pour les pages de table leaf)
            cell_pointers_offset = 8
            cells = []
            
            for i in range(cell_count):
                ptr_offset = cell_pointers_offset + i * 2
                if ptr_offset + 2 <= len(page_data):
                    cell_ptr = struct.unpack('>H', page_data[ptr_offset:ptr_offset+2])[0]
                    if cell_ptr < len(page_data):
                        cells.append(cell_ptr)
            
            # Extraire les cellules
            for cell_ptr in cells:
                if cell_ptr < len(page_data):
                    # Cellule : payload_size (varint) + rowid (varint) + payload
                    pos = cell_ptr
                    # Lire payload_size (varint)
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
                    
                    # Lire rowid (varint)
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
                    
                    # Le payload commence à pos
                    payload = page_data[pos:pos+payload_size]
                    cells.append((rowid, payload))
            
            # Stocker les données de cette page
            if cells:
                for item in cells:
                    if isinstance(item, tuple) and len(item) == 2:
                        rowid, payload = item
                        if len(payload) > 0:
                            current_tx.append((rowid, payload))
        
        offset += frame_header_size + page_size
        
        # Si commit_flag est non nul, c'est la fin d'une transaction
        if commit_flag != 0:
            if current_tx:
                transactions.append(current_tx)
            current_tx = []
    
    # Afficher les transactions trouvées
    print(f"\nNombre de transactions: {len(transactions)}")
    
    for i, tx in enumerate(transactions):
        print(f"\nTransaction {i+1}:")
        for rowid, payload in tx:
            # Afficher les premières données
            if len(payload) >= 64:
                print(f"  rowid={rowid}, len={len(payload)}, data[:64]={payload[:64].hex()}")
            else:
                print(f"  rowid={rowid}, len={len(payload)}, data={payload.hex()}")
    
    return transactions

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
