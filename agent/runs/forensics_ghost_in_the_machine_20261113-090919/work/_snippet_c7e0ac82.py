import struct

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

# Compter les ports sources et destinations
from collections import Counter
src_ports = [p['src_port'] for p in udp_packets]
dst_ports = [p['dst_port'] for p in udp_packets]

src_counts = Counter(src_ports)
dst_counts = Counter(dst_ports)

# Trouver les singletons (ports sources qui apparaissent une seule fois)
singletons = [port for port, count in src_counts.items() if count == 1]

# Extraire les paquets avec des ports singletons, triés par timestamp
singleton_data = []
for p in udp_packets:
    if p['src_port'] in singletons:
        singleton_data.append((p['ts'], p['src_port'], p['dst_port']))

singleton_data.sort(key=lambda x: x[0])

print("Singletons (src_port, dst_port):")
for ts, src, dst in singleton_data[:20]:
    print(f"  src={src}, dst={dst}")

# Vérifier si les ports de destination sont constants ou ont un pattern
print("\nPorts de destination des singletons:")
dst_ports_singletons = [dst for ts, src, dst in singleton_data]
print(f"Unique dst ports: {set(dst_ports_singletons)}")
print(f"Counts: {Counter(dst_ports_singletons)}")

# Peut-être que la clé est dans le port de destination
# Ou peut-être que c'est XOR avec quelque chose