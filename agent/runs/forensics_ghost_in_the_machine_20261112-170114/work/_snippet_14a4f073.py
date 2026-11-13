import struct
from collections import Counter

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 28:
            ip_header = pkt_data[14:34]
            src_ip = '.'.join(str(b) for b in ip_header[12:16])
            dst_ip = '.'.join(str(b) for b in ip_header[16:20])
            src_port = struct.unpack('>H', pkt_data[34:36])[0]
            dst_port = struct.unpack('>H', pkt_data[36:38])[0]
            udp_payload = pkt_data[42:]
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'src_port': src_port,
                'dst_port': dst_port,
                'payload': udp_payload
            })

# Identifier les ports fréquents (ceux qui apparaissent beaucoup)
src_ports = [p['src_port'] for p in packets]
port_counts = Counter(src_ports)

# Les 6 ports très fréquents (~64 fois) sont probablement la clé
frequent_ports = sorted([p for p, c in port_counts.items() if c >= 64])
print(f"Frequent ports (key candidates): {frequent_ports}")

# Les ports uniques (apparaissent une seule fois) sont le message
unique_ports_list = [p for p, c in port_counts.items() if c == 1]
print(f"Number of unique ports: {len(unique_ports_list)}")

# Essayer de convertir les ports uniques en ASCII (port - offset)
# D'abord, regardons la distribution des ports uniques
print(f"\nUnique ports range: {min(unique_ports_list)} - {max(unique_ports_list)}")

# Essayer différents offsets
for offset in [50000, 40000, 32768, 0]:
    chars = [chr(p - offset) if 32 <= p - offset < 127 else '?' for p in sorted(unique_ports_list)]
    result = ''.join(chars)
    print(f"\nOffset {offset}: {result[:50]}...")

# Peut-être que l'ordre d'apparition compte
# Extraire les ports uniques dans l'ordre d'apparition
unique_in_order = []
seen = set()
for p in packets:
    sp = p['src_port']
    if port_counts[sp] == 1 and sp not in seen:
        unique_in_order.append(sp)
        seen.add(sp)

print(f"\nUnique ports in order of appearance: {unique_in_order[:20]}...")

# Essayer de décoder avec l'ordre d'apparition
for offset in [50000, 40000, 32768, 0]:
    chars = [chr(p - offset) if 32 <= p - offset < 127 else '?' for p in unique_in_order]
    result = ''.join(chars)
    print(f"Order + Offset {offset}: {result[:50]}...")