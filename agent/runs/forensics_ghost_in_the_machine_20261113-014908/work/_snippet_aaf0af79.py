import struct
from collections import Counter

# Re-lire le pcap
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

# Ports fréquents (hors 9000)
frequent_non_9000 = [(p, c) for p, c in port_counts.items() if c > 1 and p != 9000]
print("Ports fréquents (hors 9000):")
for p, c in sorted(frequent_non_9000):
    print(f"  {p}: {c} fois, mod256={p%256}, chr={chr(p%256) if 32 <= p%256 < 127 else '?'}")

# Peut-être que la clé est formée par les ports fréquents dans l'ordre d'apparition
# Ou peut-être que chaque singleton est XORé avec un port fréquent spécifique

# Regardons l'ordre d'apparition des ports fréquents
print("\nOrdre d'apparition des ports fréquents (hors 9000):")
seen_freq = {}
for i, (src, dst) in enumerate(packets):
    for p in [src, dst]:
        if p != 9000 and port_counts[p] > 1:
            if p not in seen_freq:
                seen_freq[p] = i
                print(f"  Port {p} apparaît pour la première fois au paquet {i}")

# Peut-être que la clé est la séquence des ports fréquents triés par première apparition
sorted_by_first_appearance = sorted(seen_freq.items(), key=lambda x: x[1])
print("\nPorts fréquents triés par première apparition:")
for p, first_idx in sorted_by_first_appearance:
    print(f"  {p} (première apparition à {first_idx})")
