import struct

def parse_wal_detailed(wal_path="catalog.db-wal"):
    with open(wal_path, "rb") as f:
        data = f.read()
    
    page_size = struct.unpack(">I", data[8:12])[0]
    frame_header_size = 24
    frame_size = frame_header_size + page_size
    wal_start = 32
    
    num_frames = (len(data) - wal_start) // frame_size
    
    print(f"Page size: {page_size}, Frames: {num_frames}")
    
    # For each frame, parse the page as a SQLite page
    # Page type is at offset 0 of page data
    # 0x0d = leaf table b-tree page
    # 0x05 = interior table b-tree page
    # 0x0a = leaf index b-tree page
    # 0x02 = interior index b-tree page
    
    for frame_idx in range(num_frames):
        offset = wal_start + frame_idx * frame_size
        page_data = data[offset + frame_header_size:offset + frame_size]
        
        page_type = page_data[0]
        
        if page_type == 0x0d:  # Leaf table b-tree page
            # Parse cells
            # First 8 bytes: page header
            # offset 3-4: first freeblock
            # offset 5-6: number of cells
            # offset 7-8: cell content area start
            # offset 9: fragmented free bytes
            
            num_cells = struct.unpack(">H", page_data[5:7])[0]
            cell_content_start = struct.unpack(">H", page_data[8:10])[0]
            
            # Cell pointer array starts at offset 8 (after header)
            # For leaf pages, cell pointers are at offset 8 + (num_cells * 2)
            
            cell_pointers = []
            for c in range(num_cells):
                ptr_offset = 8 + c * 2
                if ptr_offset + 2 <= len(page_data):
                    cell_ptr = struct.unpack(">H", page_data[ptr_offset:ptr_offset+2])[0]
                    cell_pointers.append(cell_ptr)
            
            print(f"Frame {frame_idx}: Leaf table page, {num_cells} cells, pointers: {cell_pointers[:5]}...")
            
            # Parse each cell
            for ptr in cell_pointers:
                if ptr >= len(page_data):
                    continue
                cell_start = ptr
                
                # Cell format for table leaf:
                # varint: payload size
                # varint: rowid
                # payload: (payload_size bytes)
                
                # Read varint for payload size
                pos = cell_start
                payload_size = 0
                shift = 0
                while True:
                    b = page_data[pos]
                    pos += 1
                    payload_size |= (b & 0x7f) << shift
                    if b < 0x80:
                        break
                    shift += 7
                
                # Read varint for rowid
                rowid = 0
                shift = 0
                while True:
                    b = page_data[pos]
                    pos += 1
                    rowid |= (b & 0x7f) << shift
                    if b < 0x80:
                        break
                    shift += 7
                
                # Now read the payload
                payload = page_data[pos:pos+payload_size]
                
                # Check if this looks like a share (32 bytes of data)
                # In SQLite, a BLOB is stored as type code + data
                # Type code for BLOB is calculated as: 12 + 2*len(blob)
                # For 32-byte blob: 12 + 64 = 76
                
                if len(payload) >= 1:
                    first_byte = payload[0]
                    # Check if it could be a BLOB type code
                    if first_byte >= 12 and first_byte % 2 == 0:
                        blob_len = (first_byte - 12) // 2
                        if blob_len == 32 and len(payload) >= 1 + blob_len:
                            blob_data = payload[1:1+blob_len]
                            print(f"  Cell at {ptr}: 32-byte BLOB found: {blob_data.hex()}")
                        elif first_byte == 0:  # NULL
                            pass
                        elif first_byte < 12:  # Integer
                            pass
                        elif first_byte == 13:  # Empty string
                            pass
                        else:
                            # Could be text or other type
                            pass

parse_wal_detailed()