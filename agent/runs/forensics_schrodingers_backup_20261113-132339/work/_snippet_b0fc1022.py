import sqlite3

# Ouvrir la base de données pour voir les page numbers
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

# Obtenir les informations sur les pages
cursor.execute("SELECT name, rootpage FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables et leurs rootpages:")
for name, rootpage in tables:
    print(f"  {name}: rootpage={rootpage}")

conn.close()

# Maintenant, analyser le WAL pour mapper les pages aux tables
# Les pages dans le WAL sont numérotées. Je dois trouver quelle page contient quelle table.

# Lire le WAL et extraire les données par page
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

header_size = 32
frame_header_size = 24
page_size = 1024

num_frames = (len(data) - header_size) // (frame_header_size + page_size)

print(f"\nAnalyse des pages dans le WAL:")
page_data_map = {}

for i in range(num_frames):
    frame_offset = header_size + i * (frame_header_size + page_size)
    frame_header = data[frame_offset:frame_offset + frame_header_size]
    
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    
    page_data = data[frame_offset + frame_header_size:frame_offset + frame_header_size + page_size]
    
    if page_num not in page_data_map:
        page_data_map[page_num] = []
    
    page_data_map[page_num].append({
        'frame': i,
        'commit': commit_flag,
        'data': page_data
    })

for page_num in sorted(page_data_map.keys()):
    entries = page_data_map[page_num]
    print(f"\nPage {page_num}: {len(entries)} entrées dans le WAL")
    for entry in entries:
        print(f"  Frame {entry['frame']}, commit={entry['commit']}")
        # Afficher les premières données
        page_data = entry['data']
        if len(page_data) > 10:
            print(f"    Données: {page_data[:20].hex()}")
