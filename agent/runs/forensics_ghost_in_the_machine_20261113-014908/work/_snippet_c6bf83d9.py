import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    f.read(24)
    
    packets = []
    
    while True:
        pkt_hdr = f.read(16)
        if len(pkt_hdr) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_hdr)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 42:
            udp_start = 34
            src_port = struct.unpack('>H', pkt_data[udp_start:udp_start+2])[0]
            dst_port = struct.unpack('>H', pkt_data[udp_start+2:udp_start+4])[0]
            packets.append((src_port, dst_port))

all_ports = [p for pair in packets for p in pair]
port_counts = Counter(all_ports)

# Regrouper par count
by_count = {}
for p, c in port_counts.items():
    if c not in by_count:
        by_count[c] = []
    by_count[c].append(p)

print("Ports par nombre d'occurrences:")
for c in sorted(by_count.keys(), reverse=True):
    print(f"  {c} fois: {by_count[c]}")

# Les ports principaux (64-65 fois)
main_ports = by_count.get(64, []) + by_count.get(65, [])
print(f"\nPorts principaux (64-65 fois): {main_ports}")
print(f"Mod 256: {[p % 256 for p in main_ports]}")

# Peut-être que la clé est la séquence de ces ports dans l'ordre d'apparition
# Ou peut-être que chaque singleton est XORé avec un port principal correspondant

# Regardons l'ordre d'apparition des ports principaux
main_order = []
seen = set()
for src, dst in packets:
    for p in [src, dst]:
        if p in main_ports and p not in seen:
            main_order.append(p)
            seen.add(p)

print(f"\nOrdre d'apparition des ports principaux: {main_order}")
print(f"Mod 256: {[p % 256 for p in main_order]}")
