import struct

def parse_pcap(pcap_file):
    with open(pcap_file, 'rb') as f:
        # Magic number
        magic = f.read(4)
        print(f"Magic: {magic.hex()}")
        
        # Version major/minor
        version_major = struct.unpack('<H', f.read(2))[0]
        version_minor = struct.unpack('<H', f.read(2))[0]
        print(f"Version: {version_major}.{version_minor}")
        
        # Timezone, sigfigs, snaplen, network
        f.read(4)  # timezone
        f.read(4)  # sigfigs
        snaplen = struct.unpack('<I', f.read(4))[0]
        network = struct.unpack('<I', f.read(4))[0]
        print(f"Snaplen: {snaplen}, Network: {network}")
        
        packets = []
        while True:
            # Packet header: ts_sec, ts_usec, incl_len, orig_len
            pkt_header = f.read(16)
            if len(pkt_header) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
            
            # Packet data
            pkt_data = f.read(incl_len)
            if len(pkt_data) < incl_len:
                break
            
            packets.append((ts_sec, ts_usec, pkt_data))
        
        print(f"Total packets: {len(packets)}")
        return packets

packets = parse_pcap('capture.pcap')

# Analyser les paquets UDP (LINKTYPE_ETHERNET = 1, donc header Ethernet de 14 bytes)
udp_packets = []
for ts_sec, ts_usec, pkt_data in packets:
    if len(pkt_data) < 14 + 20 + 8:  # Ethernet + IP + UDP minimum
        continue
    
    # Ethernet header (14 bytes)
    eth_header = pkt_data[:14]
    eth_type = struct.unpack('>H', eth_header[12:14])[0]
    
    if eth_type != 0x0800:  # Not IPv4
        continue
    
    # IP header starts at byte 14
    ip_header = pkt_data[14:34]
    if ip_header[0] != 0x45:  # Not IPv4
        continue
    
    ip_protocol = ip_header[9]
    
    if ip_protocol != 17:  # UDP
        continue
    
    ip_src = '.'.join(str(b) for b in ip_header[12:16])
    ip_dst = '.'.join(str(b) for b in ip_header[16:20])
    
    # UDP header starts at byte 14 + 20 = 34
    udp_header = pkt_data[34:42]
    src_port, dst_port, udp_len, checksum = struct.unpack('>HHHH', udp_header)
    
    udp_data = pkt_data[42:]
    
    udp_packets.append({
        'ts': ts_sec + ts_usec / 1e6,
        'src_ip': ip_src,
        'dst_ip': ip_dst,
        'src_port': src_port,
        'dst_port': dst_port,
        'data': udp_data
    })

print(f"UDP packets: {len(udp_packets)}")

# Compter les ports sources
from collections import Counter
src_ports = [p['src_port'] for p in udp_packets]
port_counts = Counter(src_ports)

# Trouver les singletons (ports qui apparaissent une seule fois)
singletons = [port for port, count in port_counts.items() if count == 1]
print(f"Singleton ports: {len(singletons)}")
print(f"Singletons: {sorted(singletons)}")

# Afficher les données des paquets avec des ports singletons
singleton_data = []
for p in udp_packets:
    if p['src_port'] in singletons:
        singleton_data.append((p['ts'], p['src_port'], p['data']))

# Trier par timestamp
singleton_data.sort(key=lambda x: x[0])

print("\nSingleton packets (timestamp, src_port, data):")
for ts, port, data in singleton_data[:20]:
    print(f"  ts={ts:.6f}, port={port}, data={data[:30].hex()}")

# Afficher tous les ports et leurs comptes
print("\nTop 20 ports par fréquence:")
for port, count in port_counts.most_common(20):
    print(f"  port={port}, count={count}")