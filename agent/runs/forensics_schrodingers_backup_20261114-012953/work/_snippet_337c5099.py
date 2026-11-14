import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024

# Analyser chaque frame et afficher le contenu des pages
offset = 32
frame_num = 0

while offset + 8 <= len(data):
    page_num = struct.unpack('>I', data[offset:offset+4])[0]
    commit_flag = struct.unpack('>I', data[offset+4:offset+8])[0]
    
    if page_num > 0 and page_num < 10000:
        if offset + 8 + page_size <= len(data):
            page_data = data[offset+8:offset+8+page_size]
            
            # Afficher les premiers octets de chaque page pour comprendre la structure
            print(f"\n=== Frame {frame_num}: page={page_num}, commit={commit_flag} ===")
            print(f"Premiers 64 octets: {page_data[:64].hex()}")
            
            # Chercher des patterns intéressants
            # Les shares sont probablement des BLOBs de 32 octets
            # Cherchons des séquences de 32 octets avec un pattern spécifique
            
            # Afficher aussi les octets autour de l'offset 991
            if len(page_data) > 1023:
                print(f"Octets 991-1023: {page_data[991:1023].hex()}")
            
            offset += 8 + page_size
            frame_num += 1
        else:
            break
    else:
        offset += 1

print(f"\nTotal frames: {frame_num}")