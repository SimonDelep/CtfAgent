import struct

def parse_pcap(filename):
    with open(filename, 'rb') as f:
        # Magic number
        magic = f.read(4)
        if magic == b'\xd4\xc3\xb2\xa1':
            endian = '<'
        elif magic == b'\xa1\xb2\xc3\xd4':
            endian = '>'
        else:
            print(f"Unknown magic: {magic.hex()}")
            return []
        
        # Header
        hdr = f.read(24)
        version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack(endian + 'HHIIHH', hdr)
        
        packets = []
        while True:
            pkt_hdr = f.read(16)
            if len(pkt_hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', pkt_hdr)
            pkt_data = f.read(incl_len)
            
            packets.append({
                'ts': ts_sec * 1000000 + ts_usec,
                'data': pkt_data,
                'orig_len': orig_len
            })
    
    return packets

packets = parse_pcap('capture.pcap')
print(f"Total packets: {len(packets)}")

# Analyser les paquets UDP
udp_packets = []
for i, pkt in enumerate(packets):
    data = pkt['data']
    if len(data) < 8:
        continue
    
    # Ethernet header (14 bytes) + IP header (20 bytes minimum) + UDP header (8 bytes)
    # Network type 228 (0xe4) = IPv4
    # Skip Ethernet header
    if len(data) < 14 + 20 + 8:
        continue
    
    # IP header
    ip_start = 14
    ip_header = data[ip_start:ip_start+20]
    if len(ip_header) < 20:
        continue
    
    version_ihl = ip_header[0]
    ihl = (version_ihl & 0x0f) * 4
    protocol = ip_header[9]
    
    if protocol != 17:  # UDP
        continue
    
    udp_start = ip_start + 14 + ihl - 20  # ajustement
    # En fait, recalculons
    eth_len = 14
    ip_len = (data[eth_start := 14] & 0x0f) * 4
    udp_start = eth_len + ip_len
    
    if len(data) < udp_start + 8:
        continue
    
    udp_header = data[udp_start:udp_start+8]
    src_port, dst_port, length, checksum = struct.unpack('>HHHH', udp_header)
    
    # Payload
    payload = data[udp_start+8:]
    
    udp_packets.append({
        'idx': i,
        'ts': pkt['ts'],
        'src_port': src_port,
        'dst_port': dst_port,
        'udp_len': length,
        'checksum': checksum,
        'payload': payload,
        'payload_hex': payload.hex() if payload else ''
    })

print(f"UDP packets: {len(udp_packets)}")

# Compter les ports sources
from collections import Counter
src_ports = [p['src_port'] for p in udp_packets]
port_counts = Counter(src_ports)

# Singletons (apparaissent une seule fois)
singletons = [port for port, count in port_counts.items() if count == 1]
print(f"Singleton ports: {len(singletons)}")

# Ports fréquents
frequent = [(port, count) for port, count in port_counts.items() if count >= 60]
print(f"Frequent ports (>=60): {frequent}")

# Trier les singletons par timestamp
singleton_packets = [p for p in udp_packets if p['src_port'] in singletons]
singleton_packets.sort(key=lambda x: x['ts'])

print("\nSingleton packets (first 10):")
for p in singleton_packets[:10]:
    print(f"  idx={p['idx']}, ts={p['ts']}, src_port={p['src_port']}, checksum={p['checksum']}, payload={p['payload_hex']}")

# Regarder les checksums des singletons
singleton_checksums = [p['checksum'] for p in singleton_packets]
print(f"\nSingleton checksums: {singleton_checksums[:20]}")

# Regarder les ports de destination
dst_ports = [p['dst_port'] for p in udp_packets]
print(f"\nUnique dst_ports: {set(dst_ports)}")
