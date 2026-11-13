SCHEMA = {
  "name": "parse_wal",
  "description": "Parse le fichier catalog.db-wal pour extraire les pages SQLite et trouver les valeurs north et south",
  "parameters": {
    "properties": {
      "wal_path": {
        "description": "Chemin du fichier WAL",
        "type": "string"
      }
    },
    "type": "object"
  }
}

import struct

def main(args):
    wal_path = args.get("wal_path", "catalog.db-wal")
    
    with open(wal_path, "rb") as f:
        data = f.read()
    
    # Header WAL : 32 bytes
    # magic (4) + format (4) + page_size (4) + checkpoint (4) + salt1 (4) + salt2 (4) + checksum1 (4) + checksum2 (4)
    if len(data) < 32:
        return f"WAL trop petit: {len(data)} bytes"
    
    magic = data[:4]
    page_size = struct.unpack(">I", data[8:12])[0]
    checkpoint = struct.unpack(">I", data[12:16])[0]
    
    print(f"Magic: {magic.hex()}")
    print(f"Page size: {page_size}")
    print(f"Checkpoint: {checkpoint}")
    
    # Les frames commencent après le header (32 bytes)
    # Chaque frame: header (24 bytes) + page_data (page_size bytes)
    # Frame header: page_number (4) + salt1 (4) + salt2 (4) + checksum1 (4) + checksum2 (4) + commit_flag (4)
    
    offset = 32
    frame_num = 0
    pages = []
    
    while offset + 24 <= len(data):
        frame_header = data[offset:offset+24]
        page_number = struct.unpack(">I", frame_header[0:4])[0]
        commit_flag = struct.unpack(">I", frame_header[20:24])[0]
        
        if page_number == 0:
            break  # Fin des frames valides
        
        page_data = data[offset+24:offset+24+page_size]
        
        pages.append({
            "frame": frame_num,
            "page_number": page_number,
            "commit_flag": commit_flag,
            "data": page_data
        })
        
        offset += 24 + page_size
        frame_num += 1
    
    print(f"\nTotal frames: {frame_num}")
    
    # Afficher les pages qui contiennent des données intéressantes
    for p in pages:
        # Chercher des motifs "north" ou "south" ou des données hex
        page_data = p["data"]
        if b"north" in page_data.lower() or b"south" in page_data.lower():
            print(f"\nPage {p['page_number']} (frame {p['frame']}, commit={p['commit_flag']}):")
            # Trouver l'offset où se trouve le texte
            idx = page_data.lower().find(b"north")
            if idx == -1:
                idx = page_data.lower().find(b"south")
            if idx >= 0:
                print(f"  Contexte: {page_data[max(0,idx-20):idx+50]}")
    
    # Chercher des valeurs hexadécimales de 32 bytes (64 chars hex ou 32 bytes bruts)
    print("\n--- Recherche de données binaires ---")
    for p in pages:
        page_data = p["data"]
        # Chercher des séquences de 32 bytes qui pourraient être des shares
        # Les shares sont stockés quelque part dans la base
        if len(page_data) >= 32:
            # Afficher les premières lignes hex pour debugging
            hex_preview = page_data[:64].hex()
            print(f"Page {p['page_number']}: {hex_preview}...")
    
    return f"Extrait {len(pages)} pages"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
