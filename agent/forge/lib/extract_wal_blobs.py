SCHEMA = {
  "name": "extract_wal_blobs",
  "description": "Extrait les BLOBs des tables north et south depuis un fichier WAL SQLite en analysant les pages de type table leaf (0x0d)",
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
    
    with open(wal_path, "rb") as f:
        data = f.read()
    
    # Header WAL: 32 octets
    magic = struct.unpack(">I", data[0:4])[0]
    page_size = struct.unpack(">I", data[8:12])[0]
    
    print(f"WAL Magic: {hex(magic)}")
    print(f"Page size: {page_size}")
    
    # Chaque frame: 24 octets header + page_size octets de page
    frame_header_size = 24
    
    # Chercher les pages de type table leaf (0x0d)
    blobs = []
    
    offset = 32  # Après le header WAL
    frame_num = 0
    
    while offset + frame_header_size + page_size <= len(data):
        # Header de frame: 4 bytes page_number, 4 bytes children_count, 8 bytes salt, 4 bytes checksum
        frame_header = data[offset:offset+frame_header_size]
        page_data = data[offset+frame_header_size:offset+frame_header_size+page_size]
        
        # Type de page: premier octet
        page_type = page_data[0]
        
        if page_type == 0x0d:  # Table leaf
            # Chercher des BLOBs de 32 octets
            # Dans une page table leaf, les cellules contiennent les données
            # Format: payload_length (varint), rowid (varint), payload
            
            # Chercher des séquences de 32 octets non-nuls
            for i in range(len(page_data) - 32):
                blob_candidate = page_data[i:i+32]
                # Vérifier si c'est un BLOB plausible (pas trop de zéros)
                if sum(1 for b in blob_candidate if b != 0) > 16:
                    blobs.append((frame_num, i, blob_candidate))
        
        offset += frame_header_size + page_size
        frame_num += 1
    
    print(f"\nTotal frames: {frame_num}")
    print(f"Found {len(blobs)} potential 32-byte blobs")
    
    for frame, pos, blob in blobs[:10]:
        print(f"Frame {frame}, pos {pos}: {blob.hex()}")
    
    return blobs

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
