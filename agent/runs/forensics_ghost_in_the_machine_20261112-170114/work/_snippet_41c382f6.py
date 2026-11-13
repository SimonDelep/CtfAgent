import struct

with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    # Lisons le premier paquet en détail
    pkt_header = f.read(16)
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
    pkt_data = f.read(incl_len)
    
    print(f"Packet length: {incl_len}")
    print(f"Full packet data: {pkt_data.hex()}")
    print()
    
    # Décomposons byte par byte
    for i in range(0, len(pkt_data), 16):
        chunk = pkt_data[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"{i:04x}: {hex_str:<48} {ascii_str}")
