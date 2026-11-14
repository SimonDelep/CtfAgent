import struct
from collections import Counter

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
port_sources = []

for i in range(0, len(positions), 2):
    if i + 1 >= len(positions):
        break
    
    first_marker = positions[i]
    second_marker = positions[i+1]
    
    # Données commencent à second_marker + 4
    data_start = second_marker + 4
    
    # IP header commence à data_start + 4
    ip_start = data_start + 4
    
    # UDP header commence à ip_start + 20
    udp_start = ip_start + 20
    
    # Port source UDP est à udp_start + 0
    if udp_start + 2 <= len(data):
        port_source = struct.unpack('>H', data[udp_start:udp_start+2])[0]
        port_sources.append(port_source)

print(f"Nombre de paquets: {len(port_sources)}")
print(f"Premiers ports sources: {port_sources[:20]}")

# Compter les occurrences de chaque port
port_counts = Counter(port_sources)

print(f"\nDistribution des ports:")
singletons = [(p, c) for p, c in port_counts.items() if c == 1]
frequent = [(p, c) for p, c in port_counts.items() if c > 1]

print(f"Ports uniques (singletons): {len(singletons)}")
print(f"Ports fréquents: {frequent}")

# Afficher les ports singletons dans l'ordre d'apparition
singleton_ports_ordered = [p for p in port_sources if port_counts[p] == 1]
print(f"\nPorts singletons (ordre d'apparition, premiers 20): {singleton_ports_ordered[:20]}")
print(f"Total singletons: {len(singleton_ports_ordered)}")

# Afficher les ports fréquents dans l'ordre d'apparition
frequent_ports_ordered = []
seen = set()
for p in port_sources:
    if port_counts[p] > 1 and p not in seen:
        frequent_ports_ordered.append(p)
        seen.add(p)
print(f"Ports fréquents (ordre d'apparition): {frequent_ports_ordered}")