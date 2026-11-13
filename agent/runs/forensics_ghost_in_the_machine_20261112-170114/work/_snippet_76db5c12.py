import struct
from collections import Counter

# Lire le PCAP avec plus de détails
with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 28:
            src_port = struct.unpack('>H', pkt_data[34:36])[0]
            dst_port = struct.unpack('>H', pkt_data[36:38])[0]
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'src_port': src_port,
                'dst_port': dst_port
            })

# Regarder les ports de destination
dst_ports = [p['dst_port'] for p in packets]
dst_counts = Counter(dst_ports)
print("Destination ports:")
for port, count in sorted(dst_counts.items()):
    print(f"  {port}: {count}")

# Regarder les timestamps
timestamps = [(p['ts_sec'], p['ts_usec']) for p in packets]
print(f"\nFirst timestamp: {timestamps[0]}")
print(f"Last timestamp: {timestamps[-1]}")

# Vérifier si les timestamps ont un pattern
time_diffs = []
for i in range(1, len(timestamps)):
    diff = (timestamps[i][0] - timestamps[i-1][0]) * 1000000 + (timestamps[i][1] - timestamps[i-1][1])
    time_diffs.append(diff)

print(f"\nTime diffs (first 20): {time_diffs[:20]}")
print(f"Time diffs min: {min(time_diffs)}, max: {max(time_diffs)}")

# Peut-être que le message est encodé dans les microsecondes des timestamps
# Regardons les microsecondes des paquets avec des ports uniques
unique_ports_set = set()
port_counts = Counter(p['src_port'] for p in packets)
for p in packets:
    if port_counts[p['src_port']] == 1:
        unique_ports_set.add(p['src_port'])

print(f"\nUnique ports count: {len(unique_ports_set)}")

# Extraire les microsecondes des paquets uniques
unique_us = []
for p in packets:
    if p['src_port'] in unique_ports_set:
        unique_us.append(p['ts_usec'])

print(f"Microseconds of unique packets (first 20): {unique_us[:20]}")

# Peut-être que les microsecondes contiennent le message
# Regardons si les 3 derniers chiffres des microsecondes donnent quelque chose
us_chars = [us % 1000 for us in unique_us]
print(f"us % 1000 (first 20): {us_chars[:20]}")

# Ou peut-être les 2 derniers chiffres
us_chars2 = [us % 100 for us in unique_us]
print(f"us % 100 (first 20): {us_chars2[:20]}")