import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

marker = b'\xde\xad\xbe\xef'

# Trouver les positions des deadbeef
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Pour chaque paquet, extraire le port source
# Structure: deadbeef (4) + 2 octets + deadbeef (4) + 4 octets métadonnées + IP header (20) + UDP header (8) + payload

port_sources = []
packet_info = []

for i in range(0, len(positions), 2):
    if i + 1 >= len(positions):
        break
    
    first_marker = positions[i]
    second_marker = positions[i+1]
    
    # Données commencent à second_marker + 4
    data_start = second_marker + 4
    
    # IP header commence à data_start + 4
    ip_start = data_start + 4
    
    # Port source UDP est à ip_start + 20 + 2 = ip_start + 22
    port_source_offset = ip_start + 22
    
    if port_source_offset + 2 <= len(data):
        port_source = struct.unpack('>H', data[port_source_offset:port_source_offset+2])[0]
        port_sources.append(port_source)
        packet_info.append((i//2, port_source))

print(f"Nombre de paquets: {len(packet_info)}")
print(f"Premiers ports sources: {port_sources[:20]}")

# Compter les occurrences de chaque port
from collections import Counter
port_counts = Counter(port_sources)

print(f"\nDistribution des ports:")
print(f"Ports uniques (singletons): {len([p for p, c in port_counts.items() if c == 1])}")
print(f"Ports fréquents: {[(p, c) for p, c in port_counts.items() if c > 1]}")

# Afficher les ports singletons dans l'ordre d'apparition
singleton_ports = [p for p in port_sources if port_counts[p] == 1]
print(f"\nPorts singletons (ordre d'apparition): {singleton_ports[:20]}... ({len(singleton_ports)} total)")

# Afficher les ports fréquents dans l'ordre d'apparition
frequent_ports_ordered = []
seen = set()
for p in port_sources:
    if port_counts[p] > 1 and p not in seen:
        frequent_ports_ordered.append(p)
        seen.add(p)
print(f"Ports fréquents (ordre d'apparition): {frequent_ports_ordered}")