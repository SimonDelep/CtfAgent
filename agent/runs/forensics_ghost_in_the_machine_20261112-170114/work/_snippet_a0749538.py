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
unique_in_order = []
for idx, src, dst in src_ports_data:
    if port_counts[src] == 1:
        unique_in_order.append((idx, src, dst))

unique_values = [src for idx, src, dst in unique_in_order]

# Trier les ports uniques par valeur
sorted_unique = sorted(unique_values)
print(f"Ports uniques triés par valeur:")
print(sorted_unique[:50])

# Peut-être que les ports uniques sont des valeurs ASCII décalées ?
# Essayons de soustraire 50000 et voir si on obtient des caractères ASCII
print("\nPorts uniques triés - 50000:")
values = [p - 50000 for p in sorted_unique]
print(values[:50])

# Conversion en ASCII
ascii_chars = []
for v in values:
    if 32 <= v < 127:
        ascii_chars.append(chr(v))
    else:
        ascii_chars.append('?')
print(''.join(ascii_chars))

# Peut-être que c'est le byte de poids faible seulement ?
print("\nBytes de poids faible des ports uniques triés:")
low_bytes = [p & 0xFF for p in sorted_unique]
print(low_bytes[:50])

# Conversion en ASCII
ascii_low = []
for b in low_bytes:
    if 32 <= b < 127:
        ascii_low.append(chr(b))
    else:
        ascii_low.append('?')
print(''.join(ascii_low))

# Peut-être que c'est le byte de poids fort ?
print("\nBytes de poids fort des ports uniques triés:")
high_bytes = [(p >> 8) & 0xFF for p in sorted_unique]
print(high_bytes[:50])

# Conversion en ASCII
ascii_high = []
for b in high_bytes:
    if 32 <= b < 127:
        ascii_high.append(chr(b))
    else:
        ascii_high.append('?')
print(''.join(ascii_high))
