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

# Extraire les ports source avec leurs indices
src_ports_data = []
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
                    src_ports_data.append((i, src_port, dst_port))

# Compter les occurrences
port_counts = Counter([p[1] for p in src_ports_data])

# Ports fréquents (plus de 10 occurrences)
frequent_ports = {p: c for p, c in port_counts.items() if c > 10}
print(f"Ports fréquents (>10 occurrences): {len(frequent_ports)}")
for port, count in sorted(frequent_ports.items()):
    print(f"  Port {port}: {count} fois")

# Extraire les ports fréquents dans l'ordre d'apparition
frequent_in_order = []
for idx, src, dst in src_ports_data:
    if src in frequent_ports:
        frequent_in_order.append((idx, src, dst))

print(f"\nNombre de paquets avec ports fréquents: {len(frequent_in_order)}")

# Regardons les ports fréquents dans l'ordre
print("\nPremiers 50 ports fréquents dans l'ordre:")
for i, (idx, src, dst) in enumerate(frequent_in_order[:50]):
    print(f"  Packet {idx}: src={src}")

# Peut-être que les ports fréquents sont tous les mêmes et forment un pattern ?
# Ou peut-être que c'est le port de destination qui varie ?
# Attends, tous les ports de destination sont 9000...

# Essayons de voir si les ports fréquents ont un pattern
print("\nValeurs des ports fréquents dans l'ordre (premiers 100):")
freq_values = [src for idx, src, dst in frequent_in_order[:100]]
print(freq_values)

# Peut-être que c'est la différence entre les ports ?
diffs = [freq_values[i+1] - freq_values[i] for i in range(len(freq_values)-1)]
print(f"\nDifférences (premiers 50): {diffs[:50]}")
