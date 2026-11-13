import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024
frame_size = page_size + 24
num_frames = (len(data) - 32) // frame_size

# Analyser toutes les frames et trouver les pages avec des données non nulles
for i in range(num_frames):
    frame_start = 32 + i * frame_size
    frame_header = data[frame_start:frame_start+24]
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    commit_flag = struct.unpack('>I', frame_header[4:8])[0]
    
    page_data = data[frame_start+24:frame_start+24+page_size]
    page_type = page_data[0]
    
    if page_type == 0x0d:  # Leaf table b-tree page
        # Analyser le contenu de la page
        # Page header: 8 octets pour les leaf pages
        # byte 0: type (0x0d)
        # bytes 1-2: premier cell pointer
        # bytes 3-4: nombre de cellules
        # bytes 5-6: start de la zone de cellules
        # bytes 7-8: fragment free bytes
        
        num_cells = struct.unpack('>H', page_data[3:5])[0]
        first_cell_ptr = struct.unpack('>H', page_data[1:3])[0]
        
        # Les cellules contiennent les données
        # Pour une leaf page, chaque cellule a:
        # - 2 bytes: taille du payload
        # - 4 bytes: rowid (pour les leaf pages sans overflow)
        # - payload
        
        # Trouver toutes les cellules
        cell_pointers = []
        ptr_offset = 8  # Après le header de page
        for j in range(num_cells):
            ptr = struct.unpack('>H', page_data[ptr_offset + j*2:ptr_offset + j*2 + 2])[0]
            cell_pointers.append(ptr)
        
        # Extraire les données des cellules
        cell_data_list = []
        for ptr in cell_pointers:
            if ptr < len(page_data):
                # Lire le payload
                payload_size = struct.unpack('>H', page_data[ptr:ptr+2])[0]
                # rowid suit
                rowid = struct.unpack('>I', page_data[ptr+2:ptr+6])[0]
                # payload commence à ptr+6
                payload = page_data[ptr+6:ptr+6+payload_size]
                cell_data_list.append((rowid, payload))
        
        if cell_data_list:
            print(f"Frame {i}, page {page_num}, commit_flag={commit_flag}, num_cells={num_cells}")
            for rowid, payload in cell_data_list:
                print(f"  rowid={rowid}, payload_size={len(payload)}, payload_hex={payload.hex()[:64]}...")