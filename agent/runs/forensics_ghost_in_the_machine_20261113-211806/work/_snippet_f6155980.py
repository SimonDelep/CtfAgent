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

# Analyser le premier paquet en détail
i = 0
packet_start = positions[i] + 4
packet_end = positions[i+1] - 8
packet_data = data[packet_start:packet_end]

print(f"Longueur du paquet: {len(packet_data)}")
print(f"Données: {packet_data.hex()}")

# Chercher le champ protocole (octet 9 de l'en-tête IP)
# Mais d'abord, trouver où commence l'en-tête IP

# Essayons différentes positions pour l'en-tête IP
for ip_offset in [0, 2, 4, 6, 8]:
    if len(packet_data) < ip_offset + 20:
        continue
    ip_header = packet_data[ip_offset:ip_offset+20]
    version_ihl = ip_header[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4
    protocol = ip_header[9]
    
    if version == 4 and 5 <= ihl <= 15:
        print(f"\nIP offset {ip_offset}:")
        print(f"  Version: {version}, IHL: {ihl}")
        print(f"  Protocole: {protocol}")
        src_ip = '.'.join(str(b) for b in ip_header[12:16])
        dst_ip = '.'.join(str(b) for b in ip_header[16:20])
        print(f"  Source IP: {src_ip}")
        print(f"  Dest IP: {dst_ip}")
        
        # En-tête UDP
        udp_start = ip_offset + ihl
        if len(packet_data) >= udp_start + 8:
            udp_header = packet_data[udp_start:udp_start+8]
            src_port = struct.unpack('>H', udp_header[0:2])[0]
            dst_port = struct.unpack('>H', udp_header[2:4])[0]
            print(f"  Port source: {src_port}")
            print(f"  Port destination: {dst_port}")