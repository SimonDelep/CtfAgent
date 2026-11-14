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

# Structure: [deadbeef] [2 octets] [deadbeef] [paquet complet] [8 octets]
# positions[0] = début du premier marqueur
# positions[1] = début du deuxième marqueur (positions[0] + 4 + 2 = positions[0] + 6)
# positions[2] = début du troisième marqueur (positions[1] + 4 + taille_paquet + 8)

# Vérifions: positions[1] - positions[0] = 6 (correct, 4 + 2)
print(f"positions[1] - positions[0] = {positions[1] - positions[0]}")

# positions[2] - positions[1] devrait être 4 + taille_paquet + 8
# positions[2] - positions[1] = 102 - 46 = 56
# Donc 4 + taille_paquet + 8 = 56 => taille_paquet = 44

print(f"positions[2] - positions[1] = {positions[2] - positions[1]}")
print(f"Taille du paquet (entre les marqueurs): {positions[2] - positions[1] - 4 - 8}")

# Le paquet complet est entre positions[1]+4 et positions[2]
# Mais il y a 8 octets de fin avant le prochain marqueur
# Donc le paquet IP/UDP est entre positions[1]+4 et positions[2]-8

# Regardons le contenu du premier paquet
packet_start = positions[1] + 4
packet_end = positions[2] - 8
packet_data = data[packet_start:packet_end]
print(f"\nDonnées du premier paquet: {packet_data.hex()}")
print(f"Longueur: {len(packet_data)}")

# Le paquet commence par 08 00 45 00...
# 08 00 = EtherType (IP)
# 45 = version 4, IHL 5
# Donc l'en-tête IP commence à l'octet 2 (après 08 00)

# En-tête IP:
ip_header = packet_data[2:22]  # 20 octets
print(f"\nEn-tête IP: {ip_header.hex()}")

version_ihl = ip_header[0]
version = version_ihl >> 4
ihl = (version_ihl & 0x0F) * 4
total_length = struct.unpack('>H', ip_header[2:4])[0]
protocol = ip_header[9]
src_ip = '.'.join(str(b) for b in ip_header[12:16])
dst_ip = '.'.join(str(b) for b in ip_header[16:20])

print(f"Version: {version}, IHL: {ihl}")
print(f"Longueur totale IP: {total_length}")
print(f"Protocole: {protocol}")
print(f"Source IP: {src_ip}")
print(f"Dest IP: {dst_ip}")

# En-tête UDP commence après l'en-tête IP (20 octets pour IHL=5)
# Donc UDP start = 2 (EtherType) + 20 (IP header) = 22
udp_start = 2 + ihl
udp_header = packet_data[udp_start:udp_start+8]
print(f"\nEn-tête UDP: {udp_header.hex()}")

src_port = struct.unpack('>H', udp_header[0:2])[0]
dst_port = struct.unpack('>H', udp_header[2:4])[0]
udp_length = struct.unpack('>H', udp_header[4:6])[0]
print(f"Port source: {src_port}")
print(f"Port destination: {dst_port}")
print(f"Longueur UDP: {udp_length}")

# Payload UDP
payload = packet_data[udp_start+8:udp_start+8+udp_length-8]
print(f"Payload UDP: {payload}")