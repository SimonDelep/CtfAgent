import struct
from collections import Counter

def parse_pcap(pcap_file):
    packets = []
    with open(pcap_file, 'rb') as f:
        f.read(24)
        
        while True:
            pkt_hdr = f.read(16)
            if len(pkt_hdr) < 16:
                break
            
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_hdr)
            data = f.read(incl_len)
            
            if len(data) < 42:
                continue
            
            eth_type = struct.unpack('>H', data[12:14])[0]
            if eth_type != 0x0800:
                continue
            
            ip_proto = data[23]
            if ip_proto != 17:
                continue
            
            udp_header = data[34:42]
            src_port, dst_port, udp_len, checksum = struct.unpack('>HHHH', udp_header)
            udp_data = data[42:42+udp_len-8]
            
            packets.append({
                'src_port': src_port,
                'dst_port': dst_port,
                'udp_len': udp_len,
                'data': udp_data
            })
    
    return packets

packets = parse_pcap('capture.pcap')
src_port_counts = Counter(p['src_port'] for p in packets)

# Identify frequent ports (those with many occurrences)
frequent_ports = set(port for port, count in src_port_counts.items() if count >= 60)
print(f"Frequent ports: {frequent_ports}")

# For each singleton, find the previous packet's source port
singleton_indices = []
for i, p in enumerate(packets):
    if src_port_counts[p['src_port']] == 1:
        singleton_indices.append(i)

print(f"\nFirst 10 singleton indices: {singleton_indices[:10]}")

# Check the previous packet for each singleton
print("\nFor each singleton, check previous packet:")
for idx in singleton_indices[:10]:
    prev_port = packets[idx-1]['src_port'] if idx > 0 else None
    print(f"  Singleton at pkt {idx} (port {packets[idx]['src_port']}), previous pkt {idx-1} has port {prev_port}, is_frequent={prev_port in frequent_ports if prev_port else 'N/A'}")