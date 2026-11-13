import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver tous les marqueurs dead beef
marker = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Pour chaque paquet, extraire:
# - port source
# - ce qui est après PING (pour le timestamp/ordre)

packets_info = []

for i in range(0, len(positions), 2):
    start = positions[i]
    if start + 54 >= len(data):
        break
    
    # Port source à offset 34-35
    src_port = struct.unpack('>H', data[start+34:start+36])[0]
    
    # Ce qui est après PING (offset 46-53)
    after_ping = data[start+46:start+54]
    
    packets_info.append((i//2, src_port, after_ping))

# Trouver les singletons (ports qui n'apparaissent qu'une fois)
port_counts = Counter([p[1] for p in packets_info])
singletons = [p for p in packets_info if port_counts[p[1]] == 1]

print(f"Total paquets: {len(packets_info)}")
print(f"Nombre de singletons: {len(singletons)}")

# Afficher les singletons dans l'ordre d'apparition
print("\nSingletons (port, after_ping):")
for idx, port, after_ping in singletons[:20]:
    print(f"  Packet {idx}: port={port}, after_ping={after_ping.hex()}")

# Vérifier si after_ping contient un timestamp ou un compteur
# Regardons les valeurs after_ping pour les singletons
print("\nValeurs after_ping pour les singletons:")
for idx, port, after_ping in singletons[:10]:
    # Essayer de lire comme deux uint16
    val1 = struct.unpack('>H', after_ping[0:2])[0]
    val2 = struct.unpack('>H', after_ping[2:4])[0]
    val3 = struct.unpack('>H', after_ping[4:6])[0]
    val4 = struct.unpack('>H', after_ping[6:8])[0]
    print(f"  Packet {idx}: port={port}, vals=({val1}, {val2}, {val3}, {val4})")