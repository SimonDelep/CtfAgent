# Essai avec singletons triés par valeur
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

src_ports = []
for i in range(0, len(positions), 2):
    second_deadbeef = positions[i+1]
    offset_ip = second_deadbeef + 8
    udp_start = offset_ip + 20
    
    if udp_start + 8 <= len(data):
        udp_header = data[udp_start:udp_start+8]
        src_port = int.from_bytes(udp_header[0:2], 'big')
        src_ports.append(src_port)

port_counts = Counter(src_ports)
singletons_sorted = sorted([port for port in src_ports if port_counts[port] == 1])

print(f"Singletons triés par valeur (premiers 20): {singletons_sorted[:20]}")

# Clé "sh4dow"
key = b'sh4dow'

# Essai: XOR chaque port (2 octets) avec la clé
result_bytes = []
for port in singletons_sorted:
    port_bytes = port.to_bytes(2, 'big')
    for j, b in enumerate(port_bytes):
        key_byte = key[j % len(key)]
        result_bytes.append(b ^ key_byte)

print(f"\nRésultat XOR (bytes): {result_bytes[:50]}")
try:
    decoded = bytes(result_bytes).decode('ascii', errors='replace')
    print(f"Décodé: {decoded}")
except Exception as e:
    print(f"Erreur décodage: {e}")

# Peut-être que le flag est en hex?
print(f"\nRésultat en hex: {bytes(result_bytes).hex()[:100]}")