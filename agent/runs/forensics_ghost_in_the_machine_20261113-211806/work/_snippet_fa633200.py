import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

marker = b'\xde\xad\xbe\xef'

# Les positions des deadbeef
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Chaque paquet a deux deadbeef: un au début, un après 6 octets
# Donc les positions paires (0, 2, 4...) sont les débuts de paquets
# Et les positions impaires (1, 3, 5...) sont les marqueurs intermédiaires

print("Analyse de la structure des paquets:")
print(f"Total de deadbeef: {len(positions)}")
print(f"Nombre de paquets (deadbeef pairs): {len(positions) // 2}")

# Vérifier la structure d'un paquet
# deadbeef (4) + 2 octets + deadbeef (4) + données
# Puis 56 octets jusqu'au prochain deadbeef

# Premier paquet commence à position[0] = 40
# deadbeef à 40, puis 2 octets (41-42), puis deadbeef à 46
# Données commencent à 50

# Regardons les données du premier paquet
first_packet_start = positions[0]  # 40
second_marker = positions[1]  # 46
data_start = second_marker + 4  # 50

print(f"\nPremier paquet:")
print(f"  deadbeef à: {first_packet_start}")
print(f"  2 octets intermédiaires: {data[first_packet_start+4:first_packet_start+6].hex()}")
print(f"  deadbeef à: {second_marker}")
print(f"  Données commencent à: {data_start}")

# Les données contiennent IP header (20 octets) + UDP header (8 octets) + payload
# IP header commence à data_start
ip_header = data[data_start:data_start+20]
print(f"  IP header: {ip_header.hex()}")

# IHL (Internet Header Length) est sur l'octet 0, 4 bits supérieurs
ihl = (ip_header[0] & 0x0F) * 4
print(f"  IHL: {ihl} octets")

# Port source à l'offset 20 (dans l'IP header) + 2 (port source UDP)
# En fait, UDP header commence à data_start + 20 (si IHL=20)
udp_start = data_start + 20
port_source = struct.unpack('>H', data[udp_start:udp_start+2])[0]
port_dest = struct.unpack('>H', data[udp_start+2:udp_start+4])[0]
print(f"  Port source: {port_source}")
print(f"  Port destination: {port_dest}")

# Payload UDP
payload_start = udp_start + 8
payload = data[payload_start:payload_start+8]
print(f"  Payload (8 octets): {payload} = {payload.hex()}")