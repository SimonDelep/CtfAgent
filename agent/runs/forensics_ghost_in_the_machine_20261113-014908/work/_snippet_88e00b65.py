import struct

# Parser le pcap manuellement
with open('capture.pcap', 'rb') as f:
    # Skip global header (24 bytes)
    f.read(24)
    
    ports = []
    timestamps = []
    
    while True:
        # Packet header: ts_sec(4) + ts_usec(4) + incl_len(4) + orig_len(4) = 16 bytes
        pkt_hdr = f.read(16)
        if len(pkt_hdr) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_hdr)
        
        # Packet data
        pkt_data = f.read(incl_len)
        
        # Ethernet header (14 bytes) + IP header (20 bytes) + UDP header (8 bytes)
        # On cherche le port UDP
        if len(pkt_data) >= 42:  # 14 + 20 + 8
            # UDP header starts at byte 34 (14+20)
            udp_start = 34
            src_port = struct.unpack('>H', pkt_data[udp_start:udp_start+2])[0]
            dst_port = struct.unpack('>H', pkt_data[udp_start+2:udp_start+4])[0]
            ports.append((src_port, dst_port))
            timestamps.append(ts_sec + ts_usec/1000000)

print(f"Total paquets: {len(ports)}")

# Compter les occurrences de chaque port
from collections import Counter
all_ports = [p for pair in ports for p in pair]
port_counts = Counter(all_ports)

# Singletons (apparaissent 1x)
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"Ports singletons: {len(singletons)}")
print(f"Ports singletons: {sorted(singletons)[:20]}...")

# Ports fréquents
frequent = [(p, c) for p, c in port_counts.items() if c > 1]
print(f"Ports fréquents: {len(frequent)}")
print(f"Exemples de ports fréquents: {frequent[:10]}")
