import struct

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

# Collectons les variations de TTL et ports
tll_values = []
src_ports = []
for i, pkt in enumerate(packets):
    # IP header at offset 14
    ttl = pkt[22]  # TTL est à l'offset 8 dans l'en-tête IP (14+8=22)
    udp_start = 34  # Ethernet(14) + IP(20)
    src_port = struct.unpack('>H', pkt[udp_start:udp_start+2])[0]
    dst_port = struct.unpack('>H', pkt[udp_start+2:udp_start+4])[0]
    
    tll_values.append(ttl)
    src_ports.append(src_port)

print(f"Valeurs de TTL uniques: {sorted(set(tll_values))}")
print(f"Nombre de paquets avec TTL=64: {tll_values.count(64)}")
print(f"Nombre de paquets avec TTL=113: {tll_values.count(113)}")

print(f"\nPort source unique: {sorted(set(src_ports))}")
print(f"Nombre de ports source différents: {len(set(src_ports))}")

# Regardons la distribution des ports source
from collections import Counter
port_counts = Counter(src_ports)
print(f"\nTop 10 ports source: {port_counts.most_common(10)}")