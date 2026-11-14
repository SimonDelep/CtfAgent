import struct

def parse_wal_shares(wal_path="catalog.db-wal"):
    with open(wal_path, "rb") as f:
        data = f.read()
    
    if len(data) < 32:
        return f"File too small: {len(data)} bytes"
    
    magic = struct.unpack(">I", data[0:4])[0]
    page_size = struct.unpack(">I", data[8:12])[0]
    
    result = f"WAL Magic: 0x{magic:08x}, Page size: {page_size}\n"
    result += f"Total data: {len(data)} bytes\n"
    
    frame_header_size = 24
    frame_size = frame_header_size + page_size
    
    wal_start = 32
    remaining = len(data) - wal_start
    num_frames = remaining // frame_size
    
    result += f"Expected frames: {num_frames}\n"
    
    shares = []
    
    offset = wal_start
    for i in range(num_frames):
        if offset + frame_size > len(data):
            break
        
        frame_header = data[offset:offset + frame_header_size]
        page_data = data[offset + frame_header_size:offset + frame_size]
        
        page_num = struct.unpack(">I", frame_header[0:4])[0]
        
        for j in range(len(page_data) - 31):
            blob = page_data[j:j+32]
            shares.append((i, page_num, j, blob))
        
        offset += frame_size
    
    result += f"Found {len(shares)} potential 32-byte blobs\n"
    
    for i, (frame, page, pos, blob) in enumerate(shares[:10]):
        result += f"  Frame {frame}, Page {page}, Pos {pos}: {blob.hex()}\n"
    
    return result

print(parse_wal_shares())