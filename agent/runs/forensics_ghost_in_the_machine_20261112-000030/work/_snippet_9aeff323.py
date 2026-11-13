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

# Collectons les données: port_source -> (TTL, index_dans_pcap)
port_data = defaultdict(list)
for i, pkt in enumerate(packets):
    ttl = pkt[22]
    udp_start = 34
    src_port = struct.unpack('>H', pkt[udp_start:udp_start+2])[0]
    port_data[src_port].append((ttl, i))

# Analysons la distribution
print("Analyse par port source:")
for port in sorted(port_data.keys()):
    entries = port_data[port]
    ttls = [e[0] for e in entries]
    ttl_64 = ttls.count(64)
    ttl_113 = ttls.count(113)
    print(f"Port {port}: {len(entries)} entrées (TTL=64: {ttl_64}, TTL=113: {ttl_113})")