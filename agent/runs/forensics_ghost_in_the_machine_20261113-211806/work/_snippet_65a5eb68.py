import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

dead_beef = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(dead_beef, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Extraire tous les paquets et leurs ports sources
packets_info = []

for i in range(0, len(positions), 2):
    # Le paquet est entre positions[i]+4 et positions[i+1]-8
    # Mais vérifions d'abord
    if i + 1 >= len(positions):
        break
    
    packet_start = positions[i] + 4
    packet_end = positions[i+1] - 8
    packet_data = data[packet_start:packet_end]
    
    if len(packet_data) < 28:  # Minimum pour IP + UDP
        continue
    
    # En-tête IP commence à l'octet 4 (après 00 01 08 00)
    ip_start = 4
    if len(packet_data) < ip_start + 20:
        continue
    
    ip_header = packet_data[ip_start:ip_start+20]
    
    version_ihl = ip_header[0]
    ihl = (version_ihl & 0x0F) * 4
    protocol = ip_header[9]
    
    if protocol != 17:  # UDP
        continue
    
    # En-tête UDP commence après l'en-tête IP
    udp_start = ip_start + ihl
    if len(packet_data) < udp_start + 8:
        continue
    
    udp_header = packet_data[udp_start:udp_start+8]
    src_port = struct.unpack('>H', udp_header[0:2])[0]
    dst_port = struct.unpack('>H', udp_header[2:4])[0]
    
    packets_info.append((src_port, dst_port, i//2))

print(f"Nombre de paquets UDP extraits: {len(packets_info)}")

# Afficher les premiers paquets
for p in packets_info[:10]:
    print(f"Paquet {p[2]}: src_port={p[0]}, dst_port={p[1]}")

# Extraire les ports sources uniques et leurs fréquences
from collections import Counter
src_ports = [p[0] for p in packets_info]
port_counts = Counter(src_ports)

print(f"\nNombre de ports sources uniques: {len(port_counts)}")

# Séparer les singletons (fréquence 1) et les ports fréquents
singletons = [port for port, count in port_counts.items() if count == 1]
frequent = [port for port, count in port_counts.items() if count > 1]

print(f"Nombre de singletons: {len(singletons)}")
print(f"Nombre de ports fréquents: {len(frequent)}")

# Afficher les ports fréquents et leurs comptes
print("\nPorts fréquents:")
for port in sorted(frequent):
    print(f"  Port {port}: {port_counts[port]} occurrences")

# Afficher les singletons triés par valeur
print(f"\nSingletons (triés par valeur): {sorted(singletons)[:20]}...")