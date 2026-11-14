# Extraire les singletons dans l'ordre d'apparition
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
    first_deadbeef = positions[i]
    second_deadbeef = positions[i+1]
    offset_ip = second_deadbeef + 8
    udp_start = offset_ip + 20
    
    if udp_start + 8 <= len(data):
        udp_header = data[udp_start:udp_start+8]
        src_port = int.from_bytes(udp_header[0:2], 'big')
        src_ports.append(src_port)

port_counts = Counter(src_ports)
singletons_order = [port for port in src_ports if port_counts[port] == 1]

print(f"Nombre de singletons: {len(singletons_order)}")
print(f"Singletons (ordre d'apparition): {singletons_order}")

# Clé "sh4dow"
key = b'sh4dow'
print(f"\nClé: {key}")

# Chaque singleton est un port (2 octets). XOR chaque port avec la clé.
# Mais comment? Le port est un entier 16-bit. Peut-être que chaque octet du port est XORé avec la clé.

# Essai 1: Convertir chaque port en 2 octets (big-endian), puis XOR avec la clé répétée
result_bytes = []
for port in singletons_order:
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