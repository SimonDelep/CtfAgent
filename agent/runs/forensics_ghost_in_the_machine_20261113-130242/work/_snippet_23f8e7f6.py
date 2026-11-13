import struct

# Parser le PCAP avec le magic number 0xa1b2c3c4
with open('capture.pcap', 'rb') as f:
    # Magic number
    magic = struct.unpack('<I', f.read(4))[0]
    print(f"Magic: 0x{magic:08x}")
    
    # Version mineure, majeure, timezone, timestamp, longueur max
    f.read(2 + 2 + 4 + 4 + 4)  # 20 bytes
    
    packets = []
    while True:
        # Header de paquet : ts_sec, ts_usec, incl_len, orig_len
        header = f.read(16)
        if len(header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', header)
        
        data = f.read(incl_len)
        if len(data) < incl_len:
            break
        
        packets.append((ts_sec, ts_usec, data))
    
    print(f"Total packets: {len(packets)}")

# Analyser les premiers paquets
for i, (ts_sec, ts_usec, data) in enumerate(packets[:5]):
    print(f"\nPacket {i}: len={len(data)}")
    print("Hex:", data[:60].hex())