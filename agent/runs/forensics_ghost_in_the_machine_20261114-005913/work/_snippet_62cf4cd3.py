import struct

# Lire le fichier pcap
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Magic number custom: c4c3b2a1 (little-endian)
# En-tête global de 40 octets
# Puis paquets délimités par deadbeef

# Vérifier le magic
magic = data[:4]
print(f"Magic: {magic.hex()}")

# En-tête global de 40 octets
header = data[40:]

# Trouver tous les marqueurs deadbeef
deadbeef = b'\xbe\xef\xde\xad'
positions = []
pos = 0
while True:
    idx = header.find(deadbeef, pos)
    if idx == -1:
        break
    positions.append(idx + 40)  # offset absolu
    pos = idx + 1

print(f"Nombre de marqueurs deadbeef: {len(positions)}")
print(f"Positions des 10 premiers: {positions[:10]}")

# Chaque paquet a 2 marqueurs deadbeef
# Structure: deadbeef + 2 octets + deadbeef + 4 octets méta + IP + UDP + payload

# Extraire les ports sources UDP
# IP header commence 4 octets après le second deadbeef + 4 octets méta
# Donc: deadbeef (4) + 2 + deadbeef (4) + 4 méta = 14 octets avant l'IP
# IP header: 20 octets minimum, UDP header: 8 octets
# Port source UDP est aux octets 20+20+2 = 40-41 de l'IP (relatif au début de l'IP)

# En fait, regardons la structure plus précisément
# Après le second deadbeef, il y a 4 octets de métadonnées, puis l'IP
# L'IP header commence à offset 4+2+4+4 = 14 octets après le premier deadbeef

ports = []
timestamps = []

i = 0
while i < len(positions) - 1:
    # Premier deadbeef à positions[i]
    # Deuxième deadbeef à positions[i+1]
    
    # Entre les deux deadbeef: 2 octets
    # Après le second deadbeef: 4 octets méta, puis IP
    
    second_deadbeef_pos = positions[i+1]
    # IP commence à second_deadbeef_pos + 4 (deadbeef) + 4 (méta) = second_deadbeef_pos + 8
    
    ip_start = second_deadbeef_pos + 8
    
    # Vérifier qu'on a assez de données
    if ip_start + 28 > len(data):  # IP (20) + UDP (8) + payload (min 1)
        break
    
    # IP header: octet 0 = version+IHL, octet 12-15 = src IP, 16-19 = dst IP
    # IHL est dans les 4 bits bas de l'octet 0, multiplié par 4 pour obtenir la longueur de l'en-tête IP
    
    ihl = data[ip_start] & 0x0F
    ip_header_len = ihl * 4
    
    # Port source UDP est à ip_start + ip_header_len + 2
    udp_src_port_offset = ip_start + ip_header_len + 2
    
    if udp_src_port_offset + 2 <= len(data):
        src_port = struct.unpack('>H', data[udp_src_port_offset:udp_src_port_offset+2])[0]
        ports.append(src_port)
        
        # Timestamp: les 2 octets entre les deux deadbeef
        ts_bytes = data[positions[i]+4:positions[i]+6]
        ts = struct.unpack('>H', ts_bytes)[0]
        timestamps.append(ts)
    
    i += 2  # On traite 2 marqueurs = 1 paquet

print(f"Nombre de paquets extraits: {len(ports)}")
print(f"Ports uniques: {len(set(ports))}")

# Trouver les singletons
from collections import Counter
port_counts = Counter(ports)
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"Nombre de singletons: {len(singletons)}")
print(f"Singletons (triés par valeur): {sorted(singletons)[:20]}")

# Ports fréquents
frequent = [(p, c) for p, c in port_counts.items() if c > 1]
frequent_sorted = sorted(frequent, key=lambda x: -x[1])
print(f"Ports fréquents (top 10): {frequent_sorted[:10]}")

# Vérifier la clé "sh4dow"
# Les 6 ports les plus fréquents devraient donner "sh4dow" via port % 256
top6_ports = [p for p, c in frequent_sorted[:6]]
print(f"Top 6 ports: {top6_ports}")
key_bytes = [p % 256 for p in top6_ports]
print(f"Key bytes: {key_bytes}")
print(f"Key string: {bytes(key_bytes).decode('utf-8', errors='replace')}")
