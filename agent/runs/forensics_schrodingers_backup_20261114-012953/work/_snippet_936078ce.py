import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

# Header WAL
header = data[:32]
page_size = struct.unpack('>I', header[8:12])[0]
print(f"Page size: {page_size}")

# Analyser chaque frame
offset = 32
frame_num = 0
shares_found = []

while offset + 8 <= len(data):
    page_num = struct.unpack('>I', data[offset:offset+4])[0]
    commit_flag = struct.unpack('>I', data[offset+4:offset+8])[0]
    
    # Vérifier si c'est une frame valide (page_num raisonnable)
    if page_num > 0 and page_num < 10000:
        if offset + 8 + page_size <= len(data):
            page_data = data[offset+8:offset+8+page_size]
            
            # Chercher des BLOBs de 32 octets dans cette page
            # Les shares sont probablement stockés comme des BLOBs de 32 octets
            for i in range(len(page_data) - 31):
                blob = page_data[i:i+32]
                # Un share valide devrait avoir peu de zéros (32 octets aléatoires)
                if blob.count(b'\x00') <= 4:  # très peu de zéros
                    # Vérifier si c'est un pattern intéressant
                    shares_found.append({
                        'frame': frame_num,
                        'page': page_num,
                        'commit': commit_flag,
                        'offset': i,
                        'blob': blob,
                        'hex': blob.hex()
                    })
            
            offset += 8 + page_size
            frame_num += 1
        else:
            break
    else:
        offset += 1  # Avancer d'un octet pour chercher la prochaine frame

print(f"Total frames analysées: {frame_num}")
print(f"Shares potentiels trouvés: {len(shares_found)}")

# Afficher les shares trouvés
for s in shares_found[:30]:
    print(f"Frame {s['frame']}, page {s['page']}, commit {s['commit']}, offset {s['offset']}: {s['hex']}")