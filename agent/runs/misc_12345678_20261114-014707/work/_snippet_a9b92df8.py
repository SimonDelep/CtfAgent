# Examiner les métadonnées ID3 dans le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver la position de 'ID3'
id3_pos = data.find(b'ID3')
print(f"Position de 'ID3': {id3_pos}")

if id3_pos != -1:
    # Lire les 10 premiers octets de l'en-tête ID3
    header = data[id3_pos:id3_pos+10]
    print(f"En-tête ID3 (hex): {header.hex()}")
    print(f"En-tête ID3 (repr): {repr(header)}")
    
    # L'en-tête ID3 est: ID3, version (2 octets), flags (1 octet), taille (4 octets en synchsafe)
    # Taille est encodée en synchsafe integer (7 bits par octet)
    if len(header) >= 10:
        version = header[3:5]
        flags = header[5]
        size_bytes = header[6:10]
        print(f"Version: {version.hex()}")
        print(f"Flags: {flags:08b}")
        print(f"Taille (synchsafe): {size_bytes.hex()}")
        
        # Décoder la taille synchsafe
        size = 0
        for b in size_bytes:
            size = (size << 7) | (b & 0x7f)
        print(f"Taille décoder: {size} octets")
        
        # Lire le contenu ID3
        id3_content = data[id3_pos+10:id3_pos+10+size]
        print(f"\nContenu ID3 (premières 200 octets):")
        print(repr(id3_content[:200]))
        
        # Chercher les frames TXXX
        # Format TXXX: TXXX + taille (4 octets) + description + null + valeur
        txxx_pos = id3_content.find(b'TXXX')
        while txxx_pos != -1:
            print(f"\n--- Frame TXXX trouvée à {txxx_pos} ---")
            # Lire la taille de la frame
            frame_size = int.from_bytes(id3_content[txxx_pos+4:txxx_pos+8], 'big')
            print(f"Taille de la frame: {frame_size}")
            frame_data = id3_content[txxx_pos+8:txxx_pos+8+frame_size]
            print(f"Data de la frame: {repr(frame_data[:100])}")
            txxx_pos = id3_content.find(b'TXXX', txxx_pos+1)