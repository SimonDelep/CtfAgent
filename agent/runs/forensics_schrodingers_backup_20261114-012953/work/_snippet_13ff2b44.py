import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024

# Analyser chaque frame
offset = 32
frame_num = 0

# Collecter les données
transactions = []

while offset + 8 <= len(data):
    page_num = struct.unpack('>I', data[offset:offset+4])[0]
    commit_flag = struct.unpack('>I', data[offset+4:offset+8])[0]
    
    if page_num > 0 and page_num < 10000:
        if offset + 8 + page_size <= len(data):
            page_data = data[offset+8:offset+8+page_size]
            
            # Extraire les données à l'offset 991 si elles existent
            share_data = None
            if len(page_data) > 1023:
                share_candidate = page_data[991:1023]
                # Vérifier si c'est un share valide (commence par 23010300)
                if share_candidate[:4] == b'\x23\x01\x03\x00':
                    share_data = share_candidate
            
            transactions.append({
                'frame': frame_num,
                'page': page_num,
                'commit': commit_flag,
                'share': share_data.hex() if share_data else None
            })
            
            offset += 8 + page_size
            frame_num += 1
        else:
            break
    else:
        offset += 1

# Afficher les transactions avec des shares
print("Transactions avec shares:")
for t in transactions:
    if t['share']:
        print(f"Frame {t['frame']}: page={t['page']}, commit={t['commit']}, share={t['share']}")

# Compter les types de commit
commit_counts = {}
for t in transactions:
    c = t['commit']
    commit_counts[c] = commit_counts.get(c, 0) + 1

print(f"\nRépartition des commit_flags: {commit_counts}")