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

# Ports uniques (1 occurrence)
unique_ports = [p for p, count in port_counts.items() if count == 1]

# Extraire les ports uniques dans l'ordre d'apparition
unique_in_order = []
for idx, src, dst in src_ports_data:
    if port_counts[src] == 1:
        unique_in_order.append((idx, src, dst))

print(f"Nombre de ports uniques: {len(unique_in_order)}")

# Les ports uniques sont tous autour de 50000-51000
# Peut-être qu'on doit soustraire une base pour obtenir des caractères ASCII
# Essayons de soustraire 50000
base = 50000
print(f"\nPorts uniques - {base}:")
values = [src - base for idx, src, dst in unique_in_order]
print(values[:50])

# Essayons de convertir en ASCII
print("\nConversion en ASCII (valeurs - 50000):")
ascii_chars = []
for v in values:
    if 32 <= v < 127:
        ascii_chars.append(chr(v))
    else:
        ascii_chars.append('?')
print(''.join(ascii_chars[:50]))

# Peut-être que la base est différente ?
# Regardons la valeur minimale et maximale
min_port = min([src for idx, src, dst in unique_in_order])
max_port = max([src for idx, src, dst in unique_in_order])
print(f"\nMin port: {min_port}, Max port: {max_port}")

# Peut-être que c'est XOR avec quelque chose ?
# Ou peut-être que c'est le byte de poids faible seulement ?
print("\nBytes de poids faible des ports uniques:")
low_bytes = [src & 0xFF for idx, src, dst in unique_in_order]
print(low_bytes[:50])

# Conversion en ASCII
ascii_low = []
for b in low_bytes:
    if 32 <= b < 127:
        ascii_low.append(chr(b))
    else:
        ascii_low.append('?')
print(''.join(ascii_low[:50]))
