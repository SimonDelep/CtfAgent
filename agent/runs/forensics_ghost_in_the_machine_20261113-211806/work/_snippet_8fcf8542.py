import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

marker = b'\xde\xad\xbe\xef'

# Trouver toutes les positions des marqueurs
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

print(f"Nombre de marqueurs: {len(positions)}")

# Chaque paquet a 2 marqueurs consécutifs
# Extraire les ports sources pour chaque paire de marqueurs
ports_sources = []
paquets_info = []

i = 0
while i < len(positions) - 1:
    # Ce paquet a ses marqueurs à positions[i] et positions[i+1]
    marker1_pos = positions[i]
    marker2_pos = positions[i+1]
    
    # L'en-tête IP devrait commencer après le deuxième marqueur
    # Structure: dead beef 0002 dead beef 0001 0800 4500...
    # Après le deuxième marqueur: 0001 0800 4500...
    # 0800 est l'ether type, 4500 est le début de l'en-tête IP
    
    # Chercher le début de l'en-tête IP (0x45) après le deuxième marqueur
    ip_start = data.find(b'\x45\x00', marker2_pos)
    if ip_start == -1:
        i += 2
        continue
    
    # En-tête IP: 20 octets
    # En-tête UDP: 8 octets après IP
    udp_start = ip_start + 20
    
    if udp_start + 8 > len(data):
        break
    
    # Ports UDP
    port_src = struct.unpack('>H', data[udp_start:udp_start+2])[0]
    port_dst = struct.unpack('>H', data[udp_start+2:udp_start+4])[0]
    
    ports_sources.append(port_src)
    paquets_info.append({
        'marker1': marker1_pos,
        'marker2': marker2_pos,
        'ip_start': ip_start,
        'port_src': port_src,
        'port_dst': port_dst
    })
    
    i += 2  # Passer au paquet suivant

print(f"Nombre de paquets: {len(paquets_info)}")
print(f"Ports sources uniques: {len(set(ports_sources))}")

# Compter les occurrences
from collections import Counter
port_counts = Counter(ports_sources)
print("\nPorts les plus fréquents:")
for port, count in port_counts.most_common(15):
    print(f"  Port {port}: {count} fois")

# Identifier les singletons
singletons = [(p, c) for p, c in port_counts.items() if c == 1]
print(f"\nNombre de singletons: {len(singletons)}")
if singletons:
    print(f"Ports singletons: {[p for p, c in singletons]}")

# Identifier les ports rares (moins de 10 occurrences)
rares = [(p, c) for p, c in port_counts.items() if c < 10]
print(f"\nPorts rares (< 10 occurrences): {len(rares)}")
for p, c in sorted(rares, key=lambda x: x[1]):
    print(f"  Port {p}: {c} fois")