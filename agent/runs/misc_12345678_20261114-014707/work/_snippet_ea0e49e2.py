# Examiner le chunk LIST INFO
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver 'LIST'
list_pos = data.find(b'LIST')
print(f"Position de 'LIST': {list_pos}")

if list_pos != -1:
    # Lire le header du chunk LIST
    # Format: 'LIST' + taille (4 octets) + type (4 octets) + contenu
    header = data[list_pos:list_pos+8]
    print(f"Header LIST: {repr(header)}")
    
    # Taille du chunk
    chunk_size = int.from_bytes(data[list_pos+4:list_pos+8], 'little')
    print(f"Taille du chunk LIST: {chunk_size}")
    
    # Type du chunk (INFO)
    chunk_type = data[list_pos+8:list_pos+12]
    print(f"Type: {repr(chunk_type)}")
    
    # Contenu du chunk INFO
    info_content = data[list_pos+12:list_pos+12+chunk_size-4]  # -4 pour le type
    print(f"\nContenu INFO ({len(info_content)} octets):")
    print(f"Hex: {info_content[:100].hex()}")
    print(f"Repr: {repr(info_content[:200])}")
    
    # Chercher 'Ml81dDNAMV8=' dans le contenu INFO
    b64_in_info = info_content.find(b'Ml81dDNAMV8=')
    print(f"\nPosition de 'Ml81dDNAMV8=' dans INFO: {b64_in_info}")
    
    # Afficher le contexte
    if b64_in_info != -1:
        print(f"Contexte: {repr(info_content[max(0,b64_in_info-10):b64_in_info+20])}")