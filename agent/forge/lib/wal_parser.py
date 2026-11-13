SCHEMA = {
  "name": "wal_parser",
  "description": "Parse le fichier WAL SQLite pour extraire les BLOBs north et south dans l'ordre des transactions commitées",
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
    wal_path = args.get("wal_path", "catalog.db-wal")
    
    with open(wal_path, "rb") as f:
        data = f.read()
    
    # Header WAL: 32 bytes
    # Magic: 0x377f0682 or 0x377f0683
    # Format version, page size, checkpoint seq, etc.
    
    if len(data) < 32:
        return "WAL trop petit"
    
    magic = struct.unpack(">I", data[0:4])[0]
    page_size = struct.unpack(">I", data[8:12])[0]
    
    print(f"Magic: 0x{magic:08x}, Page size: {page_size}")
    
    # Les frames commencent après le header (32 bytes)
    # Chaque frame: header de 24 bytes + page de page_size bytes
    frame_header_size = 24
    
    offset = 32  # Après le header WAL
    frame_num = 0
    
    transactions = []  # Liste de transactions, chaque transaction contient des pages modifiées
    current_tx_pages = []
    
    while offset + frame_header_size < len(data):
        # Header de frame: 24 bytes
        # Page number (4 bytes), commit flag (4 bytes), etc.
        frame_header = data[offset:offset+frame_header_size]
        page_num = struct.unpack(">I", frame_header[0:4])[0]
        commit_flag = struct.unpack(">I", frame_header[4:8])[0]  # 1 si c'est le dernier d'une transaction
        
        page_data = data[offset+frame_header_size:offset+frame_header_size+page_size]
        
        current_tx_pages.append((page_num, page_data))
        
        if commit_flag:
            transactions.append(current_tx_pages)
            current_tx_pages = []
        
        offset += frame_header_size + page_size
        frame_num += 1
    
    print(f"Nombre de frames: {frame_num}")
    print(f"Nombre de transactions: {len(transactions)}")
    
    # Maintenant, pour chaque page, chercher les BLOBs north/south
    # Les pages de type table leaf (0x0d) contiennent les données
    all_blobs = []
    
    for tx_idx, pages in enumerate(transactions):
        print(f"\nTransaction {tx_idx + 1}: {len(pages)} pages")
        for page_num, page_data in pages:
            # Vérifier si c'est une page table leaf
            if len(page_data) > 0 and page_data[0] == 0x0d:
                # Page table leaf
                # Header: type (1 byte), first freeblock (2 bytes), num cells (2 bytes), cell content start (2 bytes), fragmented free bytes (1 byte)
                if len(page_data) >= 8:
                    num_cells = struct.unpack(">H", page_data[3:5])[0]
                    cell_content_start = struct.unpack(">H", page_data[5:7])[0]
                    
                    print(f"  Page {page_num}: table leaf, {num_cells} cellules")
                    
                    # Parser les cellules
                    # Pour chaque cellule: payload length (varint), rowid (varint), payload
                    # Le payload contient les colonnes de la table
                    
                    # Trouver les pointeurs de cellules
                    cell_pointers_offset = 8  # Après le header de page
                    cell_pointers = []
                    for i in range(num_cells):
                        if cell_pointers_offset + 2 <= len(page_data):
                            ptr = struct.unpack(">H", page_data[cell_pointers_offset:cell_pointers_offset+2])[0]
                            cell_pointers.append(ptr)
                            cell_pointers_offset += 2
                    
                    # Pour chaque cellule, extraire le payload
                    for ptr in cell_pointers:
                        if ptr < len(page_data):
                            # Lire le payload length et rowid comme varints
                            idx = ptr
                            # Varint pour payload length
                            payload_len = 0
                            shift = 0
                            while True:
                                if idx >= len(page_data):
                                    break
                                b = page_data[idx]
                                idx += 1
                                payload_len |= (b & 0x7f) << shift
                                if (b & 0x80) == 0:
                                    break
                                shift += 7
                            
                            # Varint pour rowid
                            rowid = 0
                            shift = 0
                            while True:
                                if idx >= len(page_data):
                                    break
                                b = page_data[idx]
                                idx += 1
                                rowid |= (b & 0x7f) << shift
                                if (b & 0x80) == 0:
                                    break
                                shift += 7
                            
                            # Payload
                            payload = page_data[idx:idx+payload_len]
                            
                            # Le payload contient les colonnes de la table
                            # Pour la table north/south, on s'attend à avoir des BLOBs
                            # La structure SQLite: type (varint) pour chaque colonne, puis la valeur
                            
                            # Essayer d'extraire les BLOBs
                            # Un BLOB est typiquement précédé d'un type indiquant sa longueur
                            # Type = (len * 2) + 13 pour les BLOBs (selon la spécification SQLite)
                            
                            # Pour simplifier, cherchons des séquences de 32 octets qui pourraient être nos BLOBs
                            if len(payload) >= 32:
                                # Chercher des patterns de BLOBs
                                # Dans SQLite, un BLOB de 32 octets aurait un type = 32*2 + 13 = 77
                                # Mais le format interne est plus complexe
                                
                                # Pour l'instant, affichons le payload brut
                                print(f"    Cellule rowid={rowid}, payload_len={payload_len}")
                                if len(payload) >= 32:
                                    # Essayer d'extraire des BLOBs de 32 octets
                                    # Peut-être que le payload contient directement les données
                                    # Ou peut-être qu'il y a un en-tête
                                    
                                    # Affichons les premiers octets du payload
                                    print(f"    Payload hex: {payload[:64].hex()}")
                                    
                                    # Si le payload est exactement 32 octets ou plus, on pourrait avoir nos données
                                    # Mais il faut comprendre la structure de la table
                                    
                                    # Pour une table avec colonnes north et south, le payload contient
                                    # d'abord le type de la colonne north, puis la valeur north,
                                    # puis le type de la colonne south, puis la valeur south
                                    
                                    # Essayons de parser correctement
                                    p_idx = 0
                                    columns = []
                                    while p_idx < len(payload):
                                        # Lire le type (varint)
                                        type_val = 0
                                        shift = 0
                                        start_idx = p_idx
                                        while True:
                                            if p_idx >= len(payload):
                                                break
                                            b = payload[p_idx]
                                            p_idx += 1
                                            type_val |= (b & 0x7f) << shift
                                            if (b & 0x80) == 0:
                                                break
                                            shift += 7
                                        
                                        # Déterminer la taille de la valeur
                                        if type_val == 0:
                                            # NULL
                                            columns.append(("NULL", None))
                                        elif type_val == 1:
                                            # 1 byte signed int
                                            if p_idx < len(payload):
                                                val = struct.unpack("b", payload[p_idx:p_idx+1])[0]
                                                columns.append(("int1", val))
                                                p_idx += 1
                                        elif type_val == 2:
                                            # 2 bytes signed int
                                            if p_idx + 1 < len(payload):
                                                val = struct.unpack(">h", payload[p_idx:p_idx+2])[0]
                                                columns.append(("int2", val))
                                                p_idx += 2
                                        elif type_val == 3:
                                            # 3 bytes signed int
                                            if p_idx + 2 < len(payload):
                                                val = struct.unpack(">i", b'\x00' + payload[p_idx:p_idx+3])[0]
                                                if val > 0x7fffff:
                                                    val -= 0x1000000
                                                columns.append(("int3", val))
                                                p_idx += 3
                                        elif type_val == 4:
                                            # 4 bytes signed int
                                            if p_idx + 3 < len(payload):
                                                val = struct.unpack(">i", payload[p_idx:p_idx+4])[0]
                                                columns.append(("int4", val))
                                                p_idx += 4
                                        elif type_val == 5:
                                            # 6 bytes signed int
                                            if p_idx + 5 < len(payload):
                                                val = struct.unpack(">q", b'\x00\x00' + payload[p_idx:p_idx+6])[0]
                                                columns.append(("int6", val))
                                                p_idx += 6
                                        elif type_val == 6:
                                            # 8 bytes signed int
                                            if p_idx + 7 < len(payload):
                                                val = struct.unpack(">q", payload[p_idx:p_idx+8])[0]
                                                columns.append(("int8", val))
                                                p_idx += 8
                                        elif type_val == 7:
                                            # IEEE float 8 bytes
                                            if p_idx + 7 < len(payload):
                                                val = struct.unpack(">d", payload[p_idx:p_idx+8])[0]
                                                columns.append(("float", val))
                                                p_idx += 8
                                        elif type_val == 8:
                                            # Integer 0
                                            columns.append(("int0", 0))
                                        elif type_val == 9:
                                            # Integer 1
                                            columns.append(("int1", 1))
                                        elif type_val >= 12 and type_val % 2 == 0:
                                            # BLOB: length = (type - 12) / 2
                                            blob_len = (type_val - 12) // 2
                                            if p_idx + blob_len <= len(payload):
                                                blob = payload[p_idx:p_idx+blob_len]
                                                columns.append(("BLOB", blob))
                                                p_idx += blob_len
                                        elif type_val >= 13 and type_val % 2 == 1:
                                            # TEXT: length = (type - 13) / 2
                                            text_len = (type_val - 13) // 2
                                            if p_idx + text_len <= len(payload):
                                                text = payload[p_idx:p_idx+text_len]
                                                columns.append(("TEXT", text))
                                                p_idx += text_len
                                        else:
                                            # Inconnu, avancer d'un octet
                                            p_idx += 1
                                    
                                    print(f"    Colonnes: {columns}")
                                    for col_type, col_val in columns:
                                        if col_type == "BLOB" and col_val:
                                            print(f"    BLOB trouvé: {col_val.hex()}")
                                            all_blobs.append(col_val)
    
    print(f"\nTotal de BLOBs extraits: {len(all_blobs)}")
    for i, blob in enumerate(all_blobs):
        print(f"  Blob {i}: {blob.hex()}")
    
    return all_blobs

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
