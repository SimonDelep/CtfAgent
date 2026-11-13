# Ports qui apparaissent 2-3 fois
rare_frequent = [50608, 50631, 50972]

print("Ports rares (2-3 occurrences) mod 256:")
for p in rare_frequent:
    print(f"  {p} -> {p % 256} -> {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")

# Peut-être que la clé est formée par ces ports
# 50608 % 256 = 176, 50631 % 256 = 199, 50972 % 256 = 28

# Ou peut-être que la clé est la séquence de tous les ports fréquents dans un ordre spécifique
# Regardons l'ordre d'apparition des ports rares
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

# Trouver l'ordre d'apparition des ports rares
print("\nOrdre d'apparition des ports rares:")
for i, (src, dst) in enumerate(packets):
    for p in [src, dst]:
        if p in rare_frequent:
            print(f"  Paquet {i}: port {p}")

# Peut-être que la clé est la séquence des ports rares dans l'ordre d'apparition
rare_order = []
seen = set()
for src, dst in packets:
    for p in [src, dst]:
        if p in rare_frequent and p not in seen:
            rare_order.append(p)
            seen.add(p)

print(f"\nOrdre d'apparition des ports rares: {rare_order}")
print(f"Mod 256: {[p % 256 for p in rare_order]}")
