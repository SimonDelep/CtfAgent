import struct

def parse_wal_shares(wal_path):
    with open(wal_path, 'rb') as f:
        data = f.read()
    
    if len(data) < 32:
        return "WAL too small"
    
    magic = struct.unpack('>I', data[0:4])[0]
    if magic != 0x377f0682 and magic != 0x377f0683:
        return f"Invalid WAL magic: {hex(magic)}"
    
    page_size = struct.unpack('>I', data[8:12])[0]
    
    print(f"WAL magic: {hex(magic)}, page_size: {page_size}")
    
    frame_header_size = 24
    offset = 32
    
    frames = []
    while offset + frame_header_size + page_size <= len(data):
        frame_header = data[offset:offset + frame_header_size]
        page_type = data[offset + frame_header_size]
        
        page_number = struct.unpack('>I', frame_header[0:4])[0]
        commit_flag = struct.unpack('>I', frame_header[4:8])[0]
        
        frames.append({
            'offset': offset,
            'page_number': page_number,
            'commit_flag': commit_flag,
            'page_type': page_type,
            'page_data': data[offset + frame_header_size:offset + frame_header_size + page_size]
        })
        
        offset += frame_header_size + page_size
    
    print(f"Found {len(frames)} frames")
    
    # Look for table leaf pages (0x0d) and extract 32-byte blobs
    shares = []
    for frame in frames:
        if frame['page_type'] == 0x0d:  # Table leaf page
            page_data = frame['page_data']
            i = 0
            while i < len(page_data) - 32:
                blob = page_data[i:i+32]
                if blob != b'\x00' * 32:
                    shares.append({
                        'frame_page': frame['page_number'],
                        'commit_flag': frame['commit_flag'],
                        'offset_in_page': i,
                        'blob': blob
                    })
                i += 1
    
    print(f"Found {len(shares)} potential 32-byte blobs")
    for s in shares[:10]:
        print(f"  Page {s['frame_page']}, commit={s['commit_flag']}, offset={s['offset_in_page']}: {s['blob'].hex()[:32]}...")
    
    return shares

shares = parse_wal_shares('catalog.db-wal')
print(f"\nTotal shares found: {len(shares)}")