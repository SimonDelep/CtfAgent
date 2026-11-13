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
        'udp_len': udp_len,
        'checksum': checksum,
        'data': udp_data
    })

# Compter les ports sources
src_ports = [p['src_port'] for p in udp_packets]
src_counts = Counter(src_ports)

# Trouver les singletons
singletons = [port for port, count in src_counts.items() if count == 1]

# Extraire les paquets avec des ports singletons, triés par timestamp
singleton_data = []
for p in udp_packets:
    if p['src_port'] in singletons:
        singleton_data.append((p['ts'], p['src_port']))

singleton_data.sort(key=lambda x: x[0])
singleton_ports = [port for ts, port in singleton_data]

# Convertir les ports en bytes
bytes_from_ports = []
for port in singleton_ports:
    high_byte = (port >> 8) & 0xFF
    low_byte = port & 0xFF
    bytes_from_ports.append(high_byte)
    bytes_from_ports.append(low_byte)

# Les ports fréquents: 40115, 40104, 40052, 40100, 40111, 50631, 40119, 50972, 50608
# Peut-être que la clé est la séquence de ces ports dans l'ordre d'apparition
# Ou peut-être que c'est XOR avec une clé dérivée de ces ports

# Regardons l'ordre d'apparition des ports fréquents
freq_port_order = []
for p in udp_packets:
    if p['src_port'] not in singletons:
        freq_port_order.append(p['src_port'])

print("Ordre d'apparition des ports fréquents (premiers 50):")
print(freq_port_order[:50])

# Peut-être que la clé est XOR avec le port fréquent correspondant
# Mais il y a 9 ports fréquents et 112 singletons...

# Essayons de voir si les ports fréquents forment une clé répétitive
# Ou peut-être que c'est XOR avec une clé fixe dérivée des ports fréquents

# Regardons les checksums des paquets singletons
print("\nChecksums des paquets singletons (premiers 10):")
for p in udp_packets:
    if p['src_port'] in singletons:
        print(f"  src={p['src_port']}, checksum={p['checksum']}, udp_len={p['udp_len']}")
        if len([x for x in udp_packets if x['src_port'] in singletons and x['src_port'] == p['src_port']]) == 1:
            pass  # Juste pour compter
        break