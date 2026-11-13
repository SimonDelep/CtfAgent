import struct

# Re-lisons le pcap pour analyser la structure
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Skip PCAP global header (24 bytes)
offset = 24

packets = []
while offset < len(data):
    # PCAP packet header: ts_sec(4) + ts_usec(4) + incl_len(4) + orig_len(4) = 16 bytes
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append(pkt_data)

print(f"Total packets: {len(packets)}")
print(f"First packet length: {len(packets[0])}")
print(f"First 100 bytes of first packet: {packets[0][:100].hex()}")

# Cherchons le motif "Se"
for i, pkt in enumerate(packets[:10]):
    se_pos = pkt.find(b'Se')
    if se_pos >= 0:
        print(f"Packet {i}: 'Se' at position {se_pos}")
        # Les 4 octets après "Se"
        if se_pos + 6 <= len(pkt):
            four_bytes = pkt[se_pos+2:se_pos+6]
            print(f"  4 bytes after 'Se': {four_bytes.hex()} = {list(four_bytes)}")