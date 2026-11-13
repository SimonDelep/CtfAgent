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

# Compter les ports sources
from collections import Counter
src_ports = [p['src_port'] for p in udp_packets]
port_counts = Counter(src_ports)

# Trouver les singletons
singletons = [port for port, count in port_counts.items() if count == 1]

# Extraire les paquets avec des ports singletons, triés par timestamp
singleton_data = []
for p in udp_packets:
    if p['src_port'] in singletons:
        singleton_data.append((p['ts'], p['src_port']))

singleton_data.sort(key=lambda x: x[0])

# Extraire les ports singletons dans l'ordre
singleton_ports = [port for ts, port in singleton_data]

print(f"Nombre de singletons: {len(singleton_ports)}")
print(f"Ports: {singleton_ports}")

# Convertir les ports en bytes (high byte, low byte)
# Chaque port est un entier 16 bits
bytes_from_ports = []
for port in singleton_ports:
    high_byte = (port >> 8) & 0xFF
    low_byte = port & 0xFF
    bytes_from_ports.append(high_byte)
    bytes_from_ports.append(low_byte)

print(f"\nBytes extraits: {bytes_from_ports[:40]}")
print(f"Hex: {bytes(bytes_from_ports[:40]).hex()}")

# Essayer de décoder en ASCII
try:
    text = bytes(bytes_from_ports).decode('ascii', errors='replace')
    print(f"ASCII: {text}")
except:
    print("Décodage ASCII échoué")

# Essayer de voir si c'est du XOR avec une clé
# Le hint dit que la clé est cachée dans une autre colonne
# Peut-être le port de destination ou quelque chose d'autre