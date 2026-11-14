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

# Premier paquet
first_marker = positions[0]
second_marker = positions[1]
data_start = second_marker + 4
ip_start = data_start + 4

# Afficher l'IP header complet
ip_header = data[ip_start:ip_start+20]
print("IP header (20 octets):")
print(f"  Hex: {ip_header.hex()}")

# Décomposer l'IP header
print(f"  Version/IHL: {ip_header[0]:02x} (version: {ip_header[0] >> 4}, IHL: {ip_header[0] & 0x0F})")
print(f"  Type de service: {ip_header[1]:02x}")
print(f"  Longueur totale: {struct.unpack('>H', ip_header[2:4])[0]}")
print(f"  ID: {struct.unpack('>H', ip_header[4:6])[0]}")
print(f"  Flags/Fragment: {struct.unpack('>H', ip_header[6:8])[0]}")
print(f"  TTL: {ip_header[8]}")
print(f"  Protocole: {ip_header[9]}")
print(f"  Checksum: {struct.unpack('>H', ip_header[10:12])[0]}")
print(f"  Adresse source IP: { '.'.join(str(b) for b in ip_header[12:16]) }")
print(f"  Adresse dest IP: { '.'.join(str(b) for b in ip_header[16:20]) }")

# UDP header commence à ip_start + 20
udp_start = ip_start + 20
udp_header = data[udp_start:udp_start+8]
print(f"\nUDP header (8 octets):")
print(f"  Hex: {udp_header.hex()}")
print(f"  Port source: {struct.unpack('>H', udp_header[0:2])[0]}")
print(f"  Port dest: {struct.unpack('>H', udp_header[2:4])[0]}")
print(f"  Longueur: {struct.unpack('>H', udp_header[4:6])[0]}")
print(f"  Checksum: {struct.unpack('>H', udp_header[6:8])[0]}")

# Payload
payload = data[udp_start+8:udp_start+16]
print(f"\nPayload: {payload}")