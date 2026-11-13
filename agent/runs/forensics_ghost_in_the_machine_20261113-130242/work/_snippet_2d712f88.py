import struct

def parse_pcap(filename):
    with open(filename, 'rb') as f:
        magic = f.read(4)
        endian = '<'  # little-endian
        
        # Header pcap
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

# Analyser les paquets UDP
udp_packets = []
for i, pkt in enumerate(packets):
    data = pkt['data']
    if len(data) < 14 + 20 + 8:
        continue
    
    # Ethernet header (14 bytes)
    eth_len = 14
    
    # IP header
    ip_start = eth_len
    if len(data) < ip_start + 20:
        continue
    
    ip_header = data[ip_start:ip_start+20]
    version_ihl = ip_header[0]
    ihl = (version_ihl & 0x0f) * 4
    protocol = ip_header[9]
    
    if protocol != 17:  # UDP
        continue
    
    # UDP header
    udp_start = ip_start + ihl
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

# Compter les ports sources
from collections import Counter
src_ports = [p['src_port'] for p in udp_packets]
port_counts = Counter(src_ports)

# Singletons
singletons = set(port for port, count in port_counts.items() if count == 1)

# Trier les singletons par timestamp
singleton_packets = [p for p in udp_packets if p['src_port'] in singletons]
singleton_packets.sort(key=lambda x: x['ts'])

print(f"Singleton packets: {len(singleton_packets)}")

# Regarder les checksums des singletons
print("\nChecksums des singletons (premiers 20):")
for p in singleton_packets[:20]:
    print(f"  src_port={p['src_port']}, checksum={p['checksum']}, checksum_hex={hex(p['checksum'])}")

# Vérifier si les checksums sont tous les mêmes
checksums = [p['checksum'] for p in singleton_packets]
unique_checksums = set(checksums)
print(f"\nChecksums uniques: {unique_checksums}")

# Regarder aussi les ports de destination
dst_ports = [p['dst_port'] for p in singleton_packets]
print(f"\nPorts de destination uniques: {set(dst_ports)}")

# Regarder les length
lengths = [p['udp_len'] for p in singleton_packets]
print(f"\nLengths uniques: {set(lengths)}")
