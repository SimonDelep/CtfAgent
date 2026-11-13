import struct

# Re-lire le pcap
with open('capture.pcap', 'rb') as f:
    f.read(24)  # Skip pcap header
    
    packets = []
    while True:
        ts_sec = f.read(4)
        if len(ts_sec) < 4:
            break
        ts_sec = struct.unpack('<I', ts_sec)[0]
        ts_usec = struct.unpack('<I', f.read(4))[0]
        incl_len = struct.unpack('<I', f.read(4))[0]
        orig_len = struct.unpack('<I', f.read(4))[0]
        
        data = f.read(incl_len)
        
        if len(data) >= 42:
            udp = data[34:42]
            udp_src_port = struct.unpack('>H', udp[0:2])[0]
            packets.append(udp_src_port)

print(f"Total packets: {len(packets)}")

# Regarder la séquence des ports source
print("First 50 src_ports:", packets[:50])

# Peut-être que certains ports sont des "vrais" et d'autres des leurres
# Regardons la distribution
from collections import Counter
port_counts = Counter(packets)
print("\nPort counts (first 20):")
for port, count in port_counts.most_common(20):
    print(f"  Port {port}: {count} fois")

# Peut-être que le message est dans les ports qui apparaissent une seule fois?
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"\nPorts uniques (apparaissent 1 fois): {len(singletons)}")
print(f"Singletons: {sorted(singletons)[:30]}")
