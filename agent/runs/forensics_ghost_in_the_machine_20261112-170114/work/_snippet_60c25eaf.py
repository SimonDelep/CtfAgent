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

# Peut-être que les ports uniques sont des valeurs XORées avec une clé
# La clé pourrait être dans les ports fréquents

# Regardons les ports fréquents
frequent_ports = {p: c for p, c in port_counts.items() if c > 1}
print(f"Ports fréquents: {sorted(frequent_ports.keys())}")

# Peut-être que la clé est la moyenne ou quelque chose comme ça ?
# Ou peut-être que c'est un XOR avec un port fréquent spécifique ?

# Essayons de XORer les ports uniques avec chaque port fréquent
unique_values = [src for idx, src, dst in unique_in_order]

print("\nTentative de XOR avec les ports fréquents:")
for freq_port in sorted(frequent_ports.keys()):
    xored = [v ^ freq_port for v in unique_values]
    # Vérifions si le résultat ressemble à du texte ASCII
    ascii_chars = []
    valid_count = 0
    for v in xored:
        if 32 <= v < 127:
            ascii_chars.append(chr(v))
            valid_count += 1
        else:
            ascii_chars.append('?')
    
    # Si plus de 50% sont des caractères ASCII valides, c'est intéressant
    if valid_count > len(unique_values) * 0.5:
        print(f"XOR avec {freq_port}: {''.join(ascii_chars[:50])}")
        print(f"  Valid chars: {valid_count}/{len(unique_values)}")

# Peut-être que c'est XOR avec un byte seulement ?
print("\nTentative de XOR avec des bytes (0-255):")
for key_byte in range(256):
    xored = [v ^ key_byte for v in unique_values]
    ascii_chars = []
    valid_count = 0
    for v in xored:
        if 32 <= v < 127:
            ascii_chars.append(chr(v))
            valid_count += 1
        else:
            ascii_chars.append('?')
    
    if valid_count > len(unique_values) * 0.7:
        print(f"XOR avec {key_byte} (0x{key_byte:02x}): {''.join(ascii_chars[:50])}")
        print(f"  Valid chars: {valid_count}/{len(unique_values)}")
