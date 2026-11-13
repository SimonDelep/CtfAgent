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

port_counts = Counter(p['src_port'] for p in packets)

# Regardons les ports qui apparaissent 2-3 fois
multi_ports = [(p, c) for p, c in port_counts.items() if c > 1 and c < 64]
print(f"Ports with 2-3 occurrences: {multi_ports}")

# Peut-être que ces ports sont la clé ou font partie du message
# Regardons les paquets avec ces ports
for port, count in multi_ports:
    pkts = [p for p in packets if p['src_port'] == port]
    print(f"\nPort {port} ({count} times):")
    for p in pkts:
        print(f"  ts_usec: {p['ts_usec']}, dst_port: {p['dst_port']}")

# Peut-être que le message est encodé dans les microsecondes des paquets
# Regardons les microsecondes modulo quelque chose

# Extraire tous les microsecondes
us_list = [p['ts_usec'] for p in packets]
print(f"\nMicroseconds range: {min(us_list)} - {max(us_list)}")

# Peut-être que les microsecondes modulo 256 donnent le message
us_mod256 = [us % 256 for us in us_list]
chars = [chr(b) if 32 <= b < 127 else '?' for b in us_mod256]
print(f"us % 256 (first 50): {''.join(chars[:50])}")

# Ou peut-être les microsecondes des paquets uniques seulement
unique_ports_set = set(p for p, c in port_counts.items() if c == 1)
unique_us = [p['ts_usec'] for p in packets if p['src_port'] in unique_ports_set]
print(f"\nUnique packets us count: {len(unique_us)}")

# Les microsecondes des paquets uniques modulo 256
unique_us_mod256 = [us % 256 for us in unique_us]
chars = [chr(b) if 32 <= b < 127 else '?' for b in unique_us_mod256]
print(f"Unique us % 256: {''.join(chars)}")

# Peut-être que les microsecondes modulo 128
unique_us_mod128 = [us % 128 for us in unique_us]
chars = [chr(b) if 32 <= b < 127 else '?' for b in unique_us_mod128]
print(f"Unique us % 128: {''.join(chars)}")