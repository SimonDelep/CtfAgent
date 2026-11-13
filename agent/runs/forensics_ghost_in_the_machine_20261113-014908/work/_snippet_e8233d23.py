from collections import Counter

# Re-lire pour avoir les détails
with open('capture.pcap', 'rb') as f:
    f.read(24)
    
    ports = []
    
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
            ports.append((src_port, dst_port))

# Compter les occurrences
all_ports = [p for pair in ports for p in pair]
port_counts = Counter(all_ports)

# Ports fréquents (plus de 1 occurrence)
frequent_ports = [(p, c) for p, c in port_counts.items() if c > 1]
print("Ports fréquents (port, count):")
for p, c in sorted(frequent_ports):
    print(f"  {p}: {c} fois")

# Les singletons
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"\nNombre de singletons: {len(singletons)}")

# Les singletons dans l'ordre d'apparition
singleton_order = []
seen = set()
for src, dst in ports:
    for p in [src, dst]:
        if p not in seen and port_counts[p] == 1:
            singleton_order.append(p)
            seen.add(p)

print(f"Singletons dans l'ordre d'apparition (premiers 20): {singleton_order[:20]}")
