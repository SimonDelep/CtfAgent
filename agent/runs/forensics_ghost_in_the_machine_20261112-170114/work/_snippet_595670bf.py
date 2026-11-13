import struct
from collections import Counter

# Lecture complète du PCAP
with open('capture.pcap', 'rb') as f:
    magic = struct.unpack('<I', f.read(4))[0]
    version_major, version_minor = struct.unpack('<HH', f.read(4))
    thiszone, sigfigs, snaplen = struct.unpack('<III', f.read(12))
    network = struct.unpack('<I', f.read(4))[0]
    
    packets = []
    while True:
        header = f.read(16)
        if len(header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', header)
        packet = f.read(incl_len)
        packets.append((ts_sec, ts_usec, packet))

# Extraire les adresses IP et ports
ip_data = []
for i, (ts_sec, ts_usec, packet) in enumerate(packets):
    if len(packet) >= 14:
        eth_type = struct.unpack('>H', packet[12:14])[0]
        if eth_type == 0x0800:
            ip = packet[14:]
            ip_ihl = (ip[0] & 0xF) * 4
            ip_proto = ip[9]
            
            # Adresse IP source (4 octets après l'en-tête IP)
            src_ip = '.'.join(str(b) for b in ip[12:16])
            dst_ip = '.'.join(str(b) for b in ip[16:20])
            
            if ip_proto == 17:  # UDP
                udp_start = 14 + ip_ihl
                udp = packet[udp_start:]
                if len(udp) >= 8:
                    src_port = struct.unpack('>H', udp[0:2])[0]
                    dst_port = struct.unpack('>H', udp[2:4])[0]
                    ip_data.append({
                        'idx': i,
                        'ts': ts_sec + ts_usec/1000000,
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'src_port': src_port,
                        'dst_port': dst_port
                    })

print(f"Total paquets UDP: {len(ip_data)}")

# Compter les adresses IP
src_ips = Counter([d['src_ip'] for d in ip_data])
dst_ips = Counter([d['dst_ip'] for d in ip_data])

print(f"\nAdresses IP source:")
for ip, count in src_ips.most_common(10):
    print(f"  {ip}: {count}")

print(f"\nAdresses IP destination:")
for ip, count in dst_ips.most_common(10):
    print(f"  {ip}: {count}")

# Afficher les premiers paquets
print("\nPremiers 10 paquets:")
for d in ip_data[:10]:
    print(f"  Packet {d['idx']}: {d['src_ip']}:{d['src_port']} -> {d['dst_ip']}:{d['dst_port']}")
