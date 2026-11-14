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

# Extraire les ports sources de tous les paquets
src_ports = []
payloads = []

for i in range(0, len(positions), 2):
    first_deadbeef = positions[i]
    second_deadbeef = positions[i+1]
    
    # Offset IP header = second_deadbeef + 4 + 4 = second_deadbeef + 8
    offset_ip = second_deadbeef + 8
    
    # UDP header commence à offset_ip + 20 (IP header size)
    udp_start = offset_ip + 20
    
    if udp_start + 8 <= len(data):
        udp_header = data[udp_start:udp_start+8]
        src_port = int.from_bytes(udp_header[0:2], 'big')
        src_ports.append(src_port)
        
        udp_len = int.from_bytes(udp_header[4:6], 'big')
        payload_len = udp_len - 8
        if payload_len > 0:
            payload = data[udp_start+8:udp_start+8+payload_len]
            payloads.append(payload)

print(f"Nombre de paquets: {len(src_ports)}")

# Compter les occurrences de chaque port
port_counts = Counter(src_ports)
print(f"\nNombre de ports uniques: {len(port_counts)}")

# Afficher les ports les plus fréquents
print("\nPorts les plus fréquents:")
for port, count in port_counts.most_common(15):
    print(f"  Port {port}: {count} occurrences")

# Identifier les singletons (ports qui apparaissent une seule fois)
singletons = [port for port, count in port_counts.items() if count == 1]
print(f"\nNombre de singletons: {len(singletons)}")
print(f"Singletons (triés par valeur): {sorted(singletons)[:20]}...")

# Vérifier si les singletons sont triés par timestamp (ordre d'apparition)
singleton_order = []
for port in src_ports:
    if port_counts[port] == 1:
        singleton_order.append(port)

print(f"\nSingletons dans l'ordre d'apparition (premiers 20): {singleton_order[:20]}")