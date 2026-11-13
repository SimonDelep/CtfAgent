import struct

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    # Global header (24 bytes)
    global_header = f.read(24)
    magic = struct.unpack('<I', global_header[:4])[0]
    print(f"Magic: {hex(magic)}")
    
    # Time scale (microseconds)
    ts_sec_scale = 1000000 if magic == 0xa1b2c3d4 else 1
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        # Parse IP header (à partir de l'offset Ethernet)
        # On suppose Ethernet II (14 bytes) + IP
        eth_header = pkt_data[:14]
        eth_type = struct.unpack('>H', eth_header[12:14])[0]
        
        if eth_type == 0x0800:  # IPv4
            ip_start = 14
            ip_header = pkt_data[ip_start:ip_start+20]
            ip_proto = ip_header[9]
            
            if ip_proto == 6:  # TCP
                tcp_start = ip_start + 20
                tcp_header = pkt_data[tcp_start:tcp_start+20]
                src_port = struct.unpack('>H', tcp_header[0:2])[0]
                dst_port = struct.unpack('>H', tcp_header[2:4])[0]
                
                # Payload TCP
                data_offset = (tcp_header[12] >> 4) * 4
                payload = pkt_data[tcp_start + data_offset:]
                
                packets.append({
                    'ts_sec': ts_sec,
                    'ts_usec': ts_usec,
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'payload': payload
                })

print(f"Total packets: {len(packets)}")

# Compter les ports sources
from collections import Counter
port_counts = Counter(p['src_port'] for p in packets)
print("\nPort counts:")
for port, count in port_counts.most_common():
    print(f"  {port}: {count}")
