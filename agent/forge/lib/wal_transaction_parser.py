SCHEMA = {
  "name": "wal_transaction_parser",
  "description": "Parse SQLite WAL file to extract committed transaction shares (north/south pairs) from table leaf pages",
  "parameters": {
    "properties": {
      "wal_path": {
        "description": "Path to the WAL file",
        "type": "string"
      }
    },
    "required": [
      "wal_path"
    ],
    "type": "object"
  }
}

import struct

def main(args):
    wal_path = args["wal_path"]
    
    with open(wal_path, 'rb') as f:
        data = f.read()
    
    # WAL header is 32 bytes
    # Each frame: 24 bytes header + page_size bytes of data
    # Page size from header at offset 8-9 (big-endian)
    
    if len(data) < 32:
        return "WAL too small"
    
    page_size = struct.unpack('>H', data[8:10])[0]
    print(f"Page size: {page_size}")
    
    # Number of frames
    num_frames = (len(data) - 32) // (24 + page_size)
    print(f"Number of frames: {num_frames}")
    
    # Parse each frame
    frames = []
    offset = 32
    for i in range(num_frames):
        frame_header = data[offset:offset+24]
        page_data = data[offset+24:offset+24+page_size]
        
        # Frame header: page_number (4), commit_flag (4), ...
        page_number = struct.unpack('>I', frame_header[0:4])[0]
        commit_flag = struct.unpack('>I', frame_header[4:8])[0]
        
        frames.append({
            'page_number': page_number,
            'commit_flag': commit_flag,
            'data': page_data
        })
        
        offset += 24 + page_size
    
    # Now look for table leaf pages (type 0x0d) and extract 32-byte blobs
    # Table leaf page format:
    # - Header: 8 bytes (type, cell_count, cell_content_start, fragmented_free_bytes)
    # - Cell pointer array (2 bytes each)
    # - Cell data
    
    all_blobs = []
    
    for frame in frames:
        page_data = frame['data']
        if len(page_data) < 8:
            continue
        
        page_type = page_data[0]
        
        if page_type == 0x0d:  # Table leaf page
            cell_count = struct.unpack('>H', page_data[3:5])[0]
            cell_content_start = struct.unpack('>H', page_data[5:7])[0]
            
            # Cell pointers start at offset 8
            cell_pointers = []
            for c in range(cell_count):
                ptr_offset = 8 + c * 2
                if ptr_offset + 2 <= len(page_data):
                    ptr = struct.unpack('>H', page_data[ptr_offset:ptr_offset+2])[0]
                    cell_pointers.append(ptr)
            
            # Parse each cell
            for ptr in cell_pointers:
                if ptr >= len(page_data):
                    continue
                
                # B-tree cell in table leaf: payload_length (varint), rowid (varint), payload
                pos = ptr
                
                # Read payload_length varint
                payload_len, bytes_read = read_varint(page_data, pos)
                pos += bytes_read
                
                # Read rowid varint
                rowid, bytes_read = read_varint(page_data, pos)
                pos += bytes_read
                
                # Payload starts here
                payload = page_data[pos:pos+payload_len]
                
                # Look for 32-byte blobs (shares)
                if len(payload) >= 32:
                    # Try to find 32-byte sequences that look like shares
                    # Shares are just raw bytes, so we look for any 32-byte sequence
                    # that could be a share
                    for i in range(len(payload) - 31):
                        blob = payload[i:i+32]
                        # Check if it's a valid share (all bytes, no obvious pattern)
                        all_blobs.append({
                            'frame': frame['page_number'],
                            'commit': frame['commit_flag'],
                            'rowid': rowid,
                            'blob': blob
                        })
    
    # Group blobs by transaction (commit_flag != 0 indicates end of transaction)
    # Actually, we need to understand the transaction structure better
    # Let's just return all blobs with their frame info for now
    
    result = []
    for b in all_blobs:
        result.append({
            'page': b['frame'],
            'commit': b['commit'],
            'rowid': b['rowid'],
            'blob_hex': b['blob'].hex()
        })
    
    return f"Found {len(result)} potential blobs. First 20:\n" + "\n".join(str(r) for r in result[:20])

def read_varint(data, pos):
    """Read SQLite varint, return (value, bytes_read)"""
    result = 0
    for i in range(9):
        if pos + i >= len(data):
            break
        byte = data[pos + i]
        if i < 8:
            result = (result << 7) | (byte & 0x7f)
            if byte < 0x80:
                return result, i + 1
        else:
            result = (result << 8) | byte
            return result, 9
    return result, 9

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
