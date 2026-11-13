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

# Extraire les ports source
src_ports = []
for i, (ts_sec, ts_usec, packet) in enumerate(packets):
    if len(packet) >= 14:
        eth_type = struct.unpack('>H', packet[12:14])[0]
        if eth_type == 0x0800:
            ip = packet[14:]
            ip_ihl = (ip[0] & 0xF) * 4
            ip_proto = ip[9]
            if ip_proto == 17:
                udp_start = 14 + ip_ihl
                udp = packet[udp_start:]
                if len(udp) >= 8:
                    src_port = struct.unpack('>H', udp[0:2])[0]
                    dst_port = struct.unpack('>H', udp[2:4])[0]
                    src_ports.append((i, src_port, dst_port))

print(f"Total UDP packets: {len(src_ports)}")

# Compter les ports source
port_counts = Counter([p[1] for p in src_ports])
print("\nDistribution des ports source:")
for port, count in port_counts.most_common(20):
    print(f"  Port {port}: {count} fois")

# Afficher les ports uniques
unique_ports = sorted(set([p[1] for p in src_ports]))
print(f"\nNombre de ports source uniques: {len(unique_ports)}")
print(f"Ports: {unique_ports[:50]}")

# Regarder si les ports suivent un pattern
print("\nPremiers 30 ports source:")
for i, (idx, src, dst) in enumerate(src_ports[:30]):
    print(f"  Packet {idx}: src={src}")
