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
    
    ip_src = '.'.join(str(b) for b in ip_header[12:16])
    ip_dst = '.'.join(str(b) for b in ip_header[16:20])
    
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

# Vérifier les adresses IP
ip_src = [p['src_ip'] for p in udp_packets]
ip_dst = [p['dst_ip'] for p in udp_packets]

print("Adresses IP source uniques:")
print(set(ip_src))

print("\nAdresses IP destination uniques:")
print(set(ip_dst))

# Peut-être que la clé est dans les adresses IP
# Ou peut-être que c'est XOR avec une valeur dérivée des adresses IP