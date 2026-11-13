import struct

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    # Global header (24 bytes)
    global_header = f.read(24)
    magic = struct.unpack('<I', global_header[:4])[0]
    print(f"Magic: {hex(magic)}")
    
    # 0xa1b2c3c4 = nanosecondes
    # 0xa1b2c3d4 = microsecondes
    # 0xa1b2d4c3 = nanosecondes (big endian)
    # 0xa1b2d4c3 = microsecondes (big endian)
    
    # Lisons les premiers paquets pour comprendre la structure
    for i in range(5):
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        print(f"\nPacket {i}: ts={ts_sec}.{ts_usec}, incl_len={incl_len}, orig_len={orig_len}")
        print(f"  Raw data (first 50 bytes): {pkt_data[:50].hex()}")
