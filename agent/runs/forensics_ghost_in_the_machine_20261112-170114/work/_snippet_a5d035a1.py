import struct
from collections import Counter

# Lire le PCAP et extraire toutes les informations
with open('capture.pcap', 'rb') as f:
    # Global header (24 bytes)
    global_header = f.read(24)
    magic = struct.unpack('<I', global_header[:4])[0]
    print(f"Magic: {hex(magic)}")
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        # Skip IP header (20 bytes) + UDP header (8 bytes) = 28 bytes
        # IP header starts at offset 14 (after Ethernet header)
        if len(pkt_data) >= 28:
            # IP header
            ip_header = pkt_data[14:34]
            src_ip = '.'.join(str(b) for b in ip_header[12:16])
            dst_ip = '.'.join(str(b) for b in ip_header[16:20])
            src_port = struct.unpack('>H', pkt_data[34:36])[0]
            dst_port = struct.unpack('>H', pkt_data[36:38])[0]
            udp_payload = pkt_data[42:]
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'payload': udp_payload
            })

print(f"\nTotal packets: {len(packets)}")

# Analyser les ports sources
src_ports = [p['src_port'] for p in packets]
port_counts = Counter(src_ports)

print("\nPort distribution (top 20):")
for port, count in sorted(port_counts.items(), key=lambda x: -x[1])[:20]:
    print(f"  Port {port}: {count} times")

# Ports uniques (apparaissent une seule fois)
unique_ports = [p for p, c in port_counts.items() if c == 1]
print(f"\nUnique ports count: {len(unique_ports)}")
print(f"Unique ports (sorted): {sorted(unique_ports)}")

# Ports fréquents
frequent_ports = [p for p, c in port_counts.items() if c > 1]
print(f"\nFrequent ports: {sorted(frequent_ports)}")
for p in sorted(frequent_ports):
    print(f"  Port {p}: {port_counts[p]} times")