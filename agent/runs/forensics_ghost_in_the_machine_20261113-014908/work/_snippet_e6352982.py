import struct

def parse_pcap(pcap_file):
    packets = []
    with open(pcap_file, 'rb') as f:
        f.read(24)  # Skip global header
        
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
                'data': udp_data,
                'incl_len': incl_len
            })
    
    return packets

packets = parse_pcap('capture.pcap')
from collections import Counter
src_port_counts = Counter(p['src_port'] for p in packets)

# Find singleton packets
singleton_packets = [p for p in packets if src_port_counts[p['src_port']] == 1]

print(f"Number of singleton packets: {len(singleton_packets)}")
print("\nFirst 10 singleton packets:")
for i, p in enumerate(singleton_packets[:10]):
    print(f"  src_port={p['src_port']}, dst_port={p['dst_port']}, udp_len={p['udp_len']}, incl_len={p['incl_len']}, data={p['data'].hex()}")

# Check if all singleton packets have the same data
data_counts = Counter(p['data'] for p in singleton_packets)
print(f"\nUnique data values in singleton packets: {len(data_counts)}")
for data, count in data_counts.items():
    print(f"  {data.hex()}: {count} times")