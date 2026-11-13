import struct
from collections import Counter

def parse_pcap(pcap_file):
    with open(pcap_file, 'rb') as f:
        magic = f.read(4)
        version_major = struct.unpack('<H', f.read(2))[0]
        version_minor = struct.unpack('<H', f.read(2))[0]
        f.read(4)  # timezone
        f.read(4)  # sigfigs
        snaplen = struct.unpack('<I', f.read(4))[0]
        network = struct.unpack('<I', f.read(4))[0]
        
        packets = []
        while True:
            pkt_header = f.read(16)
            if len(pkt_header) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
            pkt_data = f.read(incl_len)
            if len(pkt_data) < incl_len:
                break
            packets.append((ts_sec, ts_usec, pkt_data))
        
        return packets

packets = parse_pcap('capture.pcap')

# Analyser les paquets UDP
udp_packets = []
for ts_sec, ts_usec, pkt_data in packets:
    if len(pkt_data) < 14 + 20 + 8:
        continue
    
    eth_header = pkt_data[:14]
    eth_type = struct.unpack('>H', eth_header[12:14])[0]
    
    if eth_type != 0x0800:
        continue
    
    ip_header = pkt_data[14:34]
    if ip_header[0] != 0x45:
        continue
    
    ip_protocol = ip_header[9]
    
    if ip_protocol != 17:
        continue
    
    udp_header = pkt_data[34:42]
    src_port, dst_port, udp_len, checksum = struct.unpack('>HHHH', udp_header)
    udp_data = pkt_data[42:]
    
    udp_packets.append({
        'ts': ts_sec + ts_usec / 1e6,
        'src_port': src_port,
        'dst_port': dst_port,
        'data': udp_data
    })

# Compter les ports sources
src_ports = [p['src_port'] for p in udp_packets]
src_counts = Counter(src_ports)

# Trouver les singletons
singletons = [port for port, count in src_counts.items() if count == 1]

# Regarder les ports de destination des paquets fréquents
print("Ports de destination des paquets avec des ports sources fréquents:")
for p in udp_packets:
    if p['src_port'] not in singletons:
        print(f"  src={p['src_port']}, dst={p['dst_port']}")
        break

# Vérifier tous les ports de destination
dst_ports = [p['dst_port'] for p in udp_packets]
dst_counts = Counter(dst_ports)
print(f"\nTous les ports de destination:")
for dst, count in dst_counts.most_common(10):
    print(f"  dst={dst}, count={count}")

# Peut-être que la clé est dans les adresses IP
ip_src = [p['src_ip'] if hasattr(p, 'src_ip') else 'unknown' for p in udp_packets]