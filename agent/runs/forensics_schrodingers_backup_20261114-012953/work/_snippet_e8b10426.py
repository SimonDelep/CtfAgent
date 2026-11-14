import struct

def parse_wal_frames(wal_path="catalog.db-wal"):
    with open(wal_path, "rb") as f:
        data = f.read()
    
    page_size = struct.unpack(">I", data[8:12])[0]
    frame_header_size = 24
    frame_size = frame_header_size + page_size
    wal_start = 32
    
    num_frames = (len(data) - wal_start) // frame_size
    
    print(f"Page size: {page_size}, Frames: {num_frames}")
    
    # Pour chaque frame, extraire la page et chercher des patterns
    # Les pages de la table control contiennent l'état armed
    # Les pages de north/south contiennent les shares
    
    # D'abord, identifions les pages par leur contenu
    # Une page SQLite a un header de 100 octets pour la page 1 (avec DB header)
    # Les autres pages ont un header de page de 8 octets
    
    for frame_idx in range(num_frames):
        offset = wal_start + frame_idx * frame_size
        page_data = data[offset + frame_header_size:offset + frame_size]
        
        # Le premier octet indique le type de page
        page_type = page_data[0]
        
        # Chercher des patterns spécifiques
        # Pour la table control: on s'attend à voir des valeurs armed (0 ou 1)
        # Pour north/south: des BLOBs de 32 octets
        
        # Chercher des séquences de 32 octets qui pourraient être des shares
        # Un share est un BLOB, donc dans le format SQLite:
        # Type code = 12 + 2*32 = 76 (0x4c)
        
        # Chercher 0x4c suivi de 32 octets de données
        for i in range(len(page_data) - 32):
            if page_data[i] == 0x4c:  # BLOB de 32 octets
                blob = page_data[i+1:i+33]
                # Vérifier si c'est plausible (pas trop de nulls)
                if blob.count(0) < 28:  # Au plus 28 octets nuls
                    print(f"Frame {frame_idx}: Potential share at offset {i}: {blob.hex()}")
        
        # Chercher aussi des patterns pour armed (INTEGER 0 ou 1)
        # INTEGER 0: type code 0 (NULL) ou 1 (0)
        # INTEGER 1: type code 1 avec valeur 1
        
        # Type code 1 = INTEGER 1 octet
        for i in range(len(page_data) - 1):
            if page_data[i] == 0x01:  # INTEGER 1 octet
                val = page_data[i+1]
                if val in (0, 1):
                    print(f"Frame {frame_idx}: Potential armed={val} at offset {i}")

parse_wal_frames()