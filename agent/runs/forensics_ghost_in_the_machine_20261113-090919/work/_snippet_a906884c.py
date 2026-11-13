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

# Les ports fréquents pourraient contenir la clé
frequent_ports = [port for port, count in src_counts.items() if count > 1]
print(f"Frequent ports: {frequent_ports}")

# Peut-être que la clé est la moyenne ou quelque chose comme ça
# Ou peut-être que c'est XOR avec un port fréquent

# Essayons de XORer les bytes avec différents ports fréquents
for freq_port in frequent_ports:
    key_high = (freq_port >> 8) & 0xFF
    key_low = freq_port & 0xFF
    
    # Essayer de XORer avec le high byte
    decrypted = []
    for i, b in enumerate(bytes_from_ports):
        if i % 2 == 0:
            decrypted.append(b ^ key_high)
        else:
            decrypted.append(b ^ key_low)
    
    try:
        text = bytes(decrypted).decode('ascii', errors='replace')
        if 'csaw' in text.lower() or 'flag' in text.lower() or '{' in text:
            print(f"XOR avec {freq_port} (high={key_high}, low={key_low}): {text[:50]}")
    except:
        pass

# Peut-être que la clé est dans les ports fréquents eux-mêmes
# Regardons les ports fréquents en hex
print("\nPorts fréquents en hex:")
for p in frequent_ports:
    print(f"  {p} = {hex(p)} = bytes: {[(p >> 8) & 0xFF, p & 0xFF]}")

# Peut-être que la clé est une séquence de bytes dérivée des ports fréquents
# Ou peut-être que c'est XOR avec une clé fixe