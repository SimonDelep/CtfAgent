import struct

# Lire le pcap et extraire les ports sources dans l'ordre
with open('capture.pcap', 'rb') as f:
    # Header pcap
    magic = f.read(4)
    version_major = struct.unpack('<H', f.read(2))[0]
    version_minor = struct.unpack('<H', f.read(2))[0]
    thiszone = struct.unpack('<i', f.read(4))[0]
    sigfigs = struct.unpack('<I', f.read(4))[0]
    snaplen = struct.unpack('<I', f.read(4))[0]
    network = struct.unpack('<I', f.read(4))[0]
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        # Ethernet header (14 bytes) + IP header (20 bytes) + UDP header (8 bytes)
        # Skip Ethernet (14), IP (20), get UDP source port (bytes 4-5 of UDP header)
        # Structure: Ethernet(14) + IP(20) + UDP(8) + data
        if len(pkt_data) >= 42:  # 14 + 20 + 8 = 42
            # IP header starts at byte 14
            ip_header = pkt_data[14:34]
            ip_proto = ip_header[9]
            if ip_proto == 17:  # UDP
                udp_start = 34
                src_port = struct.unpack('>H', pkt_data[udp_start:udp_start+2])[0]
                dst_port = struct.unpack('>H', pkt_data[udp_start+2:udp_start+4])[0]
                packets.append((src_port, dst_port))

print(f"Total packets: {len(packets)}")

# Compter les occurrences de chaque port source
from collections import Counter
src_ports = [p[0] for p in packets]
counts = Counter(src_ports)

# Trouver les singletons (port qui apparaît une seule fois)
singletons = [port for port, count in counts.items() if count == 1]
frequent = [(port, count) for port, count in counts.items() if count >= 60]

print(f"Singletons: {len(singletons)}")
print(f"Frequent ports (>=60): {frequent}")

# Ports singletons dans l'ordre d'apparition
singleton_order = []
seen = set()
for port in src_ports:
    if counts[port] == 1 and port not in seen:
        singleton_order.append(port)
        seen.add(port)

print(f"Singletons in order: {singleton_order[:20]}...")
print(f"Total singletons in order: {len(singleton_order)}")

# Ports fréquents dans l'ordre d'apparition
frequent_ports = [p[0] for p in frequent]
frequent_order = []
seen = set()
for port in src_ports:
    if port in frequent_ports and port not in seen:
        frequent_order.append(port)
        seen.add(port)

print(f"Frequent ports in order of first appearance: {frequent_order}")