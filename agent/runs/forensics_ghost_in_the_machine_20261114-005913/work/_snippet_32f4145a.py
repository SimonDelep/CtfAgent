# Extraire tous les payloads et voir s'il y a des variations
import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    data = f.read()

deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    pos = data.find(deadbeef, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

all_payloads = []
for i in range(0, len(positions), 2):
    second_deadbeef = positions[i+1]
    offset_ip = second_deadbeef + 8
    udp_start = offset_ip + 20
    
    if udp_start + 8 <= len(data):
        udp_header = data[udp_start:udp_start+8]
        src_port = int.from_bytes(udp_header[0:2], 'big')
        udp_len = int.from_bytes(udp_header[4:6], 'big')
        payload_len = udp_len - 8
        if payload_len > 0:
            payload = data[udp_start+8:udp_start+8+payload_len]
            all_payloads.append((src_port, payload))

# Compter les payloads uniques
payload_counts = Counter([p[1] for p in all_payloads])
print(f"Payloads uniques: {len(payload_counts)}")
for payload, count in payload_counts.most_common(5):
    print(f"  {payload}: {count} fois")

# Vérifier si tous les payloads sont "PING"
ping_count = sum(1 for p in all_payloads if p[1] == b'PING')
print(f"\nNombre de payloads 'PING': {ping_count}/{len(all_payloads)}")

# Peut-être que les singletons ont des payloads différents?
port_counts = Counter([p[0] for p in all_payloads])
singleton_ports = set([port for port, count in port_counts.items() if count == 1])

singleton_payloads = [p[1] for p in all_payloads if p[0] in singleton_ports]
print(f"\nPayloads des singletons (uniques): {set(singleton_payloads)}")