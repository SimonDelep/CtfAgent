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

# Ports qui n'apparaissent qu'une seule fois
single_occurrence_ports = [p for p, count in port_counts.items() if count == 1]
print(f"Ports avec une seule occurrence: {len(single_occurrence_ports)}")
print(f"Ports: {sorted(single_occurrence_ports)}")

# Extraire les ports uniques dans l'ordre d'apparition
unique_in_order = []
for idx, src, dst in src_ports_data:
    if port_counts[src] == 1:
        unique_in_order.append((idx, src, dst))

print(f"\nPorts uniques dans l'ordre:")
for idx, src, dst in unique_in_order:
    print(f"  Packet {idx}: src={src}")

# Essayer de convertir les ports en ASCII
print("\nConversion des ports uniques en ASCII (bytes):")
ascii_chars = []
for idx, src, dst in unique_in_order:
    # Le port est un entier 16 bits, essayons de le décomposer en 2 bytes
    byte1 = (src >> 8) & 0xFF
    byte2 = src & 0xFF
    ascii_chars.append((byte1, byte2))
    print(f"  Port {src} -> bytes: {byte1} ({chr(byte1) if 32 <= byte1 < 127 else '?'}) , {byte2} ({chr(byte2) if 32 <= byte2 < 127 else '?'})")

# Essayons de lire les ports comme des caractères ASCII
print("\nTentative de lecture des ports comme ASCII:")
port_values = [src for idx, src, dst in unique_in_order]
print(f"Valeurs des ports: {port_values}")

# Peut-être que les ports sont des valeurs ASCII décalées ?
# Ou peut-être que c'est le port de destination qui varie ?
dst_ports = [dst for idx, src, dst in src_ports_data]
dst_counts = Counter(dst_ports)
print(f"\nPorts de destination: {dst_counts}")
