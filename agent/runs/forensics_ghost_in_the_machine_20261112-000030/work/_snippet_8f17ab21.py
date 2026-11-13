import struct
from collections import defaultdict

# Re-lisons le pcap
with open('capture.pcap', 'rb') as f:
    data = f.read()

offset = 24
packets = []
while offset < len(data):
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append(pkt_data)

# Collectons les données des paquets avec TTL=113
signal_data = []
for i, pkt in enumerate(packets):
    ttl = pkt[22]
    if ttl == 113:
        udp_start = 34
        src_port = struct.unpack('>H', pkt[udp_start:udp_start+2])[0]
        dst_port = struct.unpack('>H', pkt[udp_start+2:udp_start+4])[0]
        # Le payload UDP
        payload = pkt[udp_start+8:]
        signal_data.append({
            'index': i,
            'src_port': src_port,
            'dst_port': dst_port,
            'payload': payload
        })

print(f"Nombre de paquets signal (TTL=113): {len(signal_data)}")
print("\nDétails des paquets signal:")
for d in signal_data:
    print(f"  Index {d['index']}: src_port={d['src_port']}, dst_port={d['dst_port']}, payload={d['payload']}")