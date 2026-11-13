import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024
frame_size = page_size + 24
num_frames = (len(data) - 32) // frame_size

# Collecter toutes les cellules avec leurs informations
all_cells = []

for i in range(num_frames):
    frame_start = 32 + i * frame_size
    frame_header = data[frame_start:frame_start+24]
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    
    page_data = data[frame_start+24:frame_start+24+page_size]
    page_type = page_data[0]
    
    if page_type == 0x0d:  # Leaf table b-tree page
        num_cells = struct.unpack('>H', page_data[3:5])[0]
        
        # Extraire les pointeurs de cellules
        cell_pointers = []
        ptr_offset = 8
        for j in range(num_cells):
            ptr = struct.unpack('>H', page_data[ptr_offset + j*2:ptr_offset + j*2 + 2])[0]
            cell_pointers.append(ptr)
        
        # Extraire les données des cellules
        for ptr in cell_pointers:
            if ptr < len(page_data):
                payload_size = struct.unpack('>H', page_data[ptr:ptr+2])[0]
                rowid = struct.unpack('>I', page_data[ptr+2:ptr+6])[0]
                payload = page_data[ptr+6:ptr+6+payload_size]
                all_cells.append({
                    'frame': i,
                    'page': page_num,
                    'commit_flag': commit_flag,
                    'rowid': rowid,
                    'payload_size': payload_size,
                    'payload': payload
                })

# Afficher les cellules par page
pages_data = {}
for cell in all_cells:
    page = cell['page']
    if page not in pages_data:
        pages_data[page] = []
    pages_data[page].append(cell)

for page in sorted(pages_data.keys()):
    print(f"\n=== Page {page} ===")
    cells = pages_data[page]
    # Regrouper par rowid
    rowid_data = {}
    for c in cells:
        if c['rowid'] not in rowid_data:
            rowid_data[c['rowid']] = []
        rowid_data[c['rowid']].append(c)
    
    for rowid in sorted(rowid_data.keys()):
        entries = rowid_data[rowid]
        print(f"  rowid={rowid}: {len(entries)} entrées")
        for e in entries:
            print(f"    frame={e['frame']}, commit_flag={e['commit_flag']}, payload_size={e['payload_size']}, payload_hex={e['payload'].hex()[:40]}...")