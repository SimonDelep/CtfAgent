import struct

# Lire le pcap manuellement pour extraire tous les singletons dans l'ordre
with open('capture.pcap', 'rb') as f:
    # Magic number
    magic = f.read(4)
    print(f"Magic: {magic.hex()}")
    
    # Global header (24 bytes)
    global_header = f.read(24)
    
    packets = []
    while True:
        # Packet header (16 bytes)
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        # Parse Ethernet + IP + UDP
        # Ethernet header: 14 bytes
        if len(pkt_data) >= 14:
            eth = pkt_data[:14]
            ether_type = struct.unpack('>H', eth[12:14])[0]
            
            if ether_type == 0x0800:  # IPv4
                ip_start = 14
                ip = pkt_data[ip_start:ip_start+20]
                if len(ip) >= 20:
                    protocol = ip[9]
                    if protocol == 17:  # UDP
                        udp_start = ip_start + 20
                        udp = pkt_data[udp_start:udp_start+8]
                        if len(udp) >= 8:
                            src_port = struct.unpack('>H', udp[0:2])[0]
                            dst_port = struct.unpack('>H', udp[2:4])[0]
                            packets.append((ts_sec, ts_usec, src_port, dst_port))

# Compter les occurrences de chaque port source
from collections import Counter
src_ports = [p[2] for p in packets]
port_counts = Counter(src_ports)

# Trouver les singletons (ports qui apparaissent une seule fois)
singletons = [port for port, count in port_counts.items() if count == 1]
print(f"Total packets: {len(packets)}")
print(f"Unique src ports: {len(port_counts)}")
print(f"Singletons count: {len(singletons)}")

# Trier les singletons par timestamp
singleton_packets = [(ts, port) for ts, ts_usec, port, dst in packets if port_counts[port] == 1]
singleton_packets.sort(key=lambda x: (x[0], x[1]))

print("\nFirst 20 singletons (timestamp, port):")
for ts, port in singleton_packets[:20]:
    print(f"  ts={ts}, port={port}")

print(f"\nAll singleton ports in order:")
ports_list = [port for ts, port in singleton_packets]
print(ports_list)