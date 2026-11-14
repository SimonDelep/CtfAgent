import struct

# Lire le fichier binaire
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Magic number custom: c4c3b2a1 (little-endian)
# En-tête global PCAP (24 octets)
# Puis chaque paquet est précédé de "dead beef" (4 octets)

# D'abord, sautons l'en-tête global (24 octets)
offset = 24

# Liste pour stocker les ports sources
ports_sources = []
paquets_info = []

# Chercher tous les marqueurs "dead beef"
marker = b'\xde\xad\xbe\xef'

pos = 0
while pos < len(data) - 4:
    # Chercher le marqueur
    idx = data.find(marker, pos)
    if idx == -1:
        break
    
    # Après le marqueur, il y a d'autres données avant l'en-tête IP
    # Structure observée: dead beef 0002 dead beef 0001 0800 4500...
    # L'en-tête IP commence par 0x45 (version 4, IHL 5)
    
    # Chercher le début de l'en-tête IP (0x45)
    ip_start = data.find(b'\x45\x00', idx)
    if ip_start == -1:
        pos = idx + 4
        continue
    
    # En-tête IP: 20 octets minimum
    # Offset 0: version + IHL
    # Offset 8: TTL
    # Offset 9: protocole (17 = UDP)
    # Offset 12-15: IP source
    # Offset 16-19: IP dest
    
    # En-tête UDP commence 20 octets après le début IP (sans options)
    udp_start = ip_start + 20
    
    if udp_start + 8 > len(data):
        break
    
    # Ports UDP: 2 octets source, 2 octets dest
    port_src = struct.unpack('>H', data[udp_start:udp_start+2])[0]
    port_dst = struct.unpack('>H', data[udp_start+2:udp_start+4])[0]
    
    # Payload UDP: 2 octets longueur, 2 octets checksum, puis données
    udp_len = struct.unpack('>H', data[udp_start+4:udp_start+6])[0]
    
    ports_sources.append(port_src)
    paquets_info.append({
        'offset': idx,
        'ip_start': ip_start,
        'port_src': port_src,
        'port_dst': port_dst,
        'udp_len': udp_len
    })
    
    pos = idx + 4

print(f"Nombre de paquets: {len(paquets_info)}")
print(f"Ports sources uniques: {len(set(ports_sources))}")

# Compter les occurrences de chaque port
from collections import Counter
port_counts = Counter(ports_sources)
print("\nPorts les plus fréquents:")
for port, count in port_counts.most_common(15):
    print(f"  Port {port}: {count} fois")

# Identifier les singletons (ports qui n'apparaissent qu'une fois)
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"\nNombre de singletons: {len(singletons)}")
print(f"Ports singletons: {sorted(singletons)[:20]}...")

# Afficher les ports dans l'ordre d'apparition
print("\nPremiers 20 ports dans l'ordre:")
print(ports_sources[:20])