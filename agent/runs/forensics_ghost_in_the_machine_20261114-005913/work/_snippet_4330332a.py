# Extraction des ports sources et payloads
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

# Les paquets commencent aux positions paires de positions (0, 2, 4, ...)
# Structure: deadbeef + 2b + deadbeef + 4b + IP + UDP + payload
# Donc le début de l'IP est à position + 4 + 2 + 4 = position + 10

packets = []
for i in range(0, len(positions), 2):
    start = positions[i]
    # Après les deux deadbeef et les 6 octets de méta, on est à start + 4 + 2 + 4 = start + 10
    ip_start = start + 10
    
    # Vérifier qu'on a assez de données
    if ip_start + 28 > len(data):  # IP (20) + UDP (8) + au moins 1 octet
        continue
    
    # Lire l'en-tête IP
    ip_header = data[ip_start:ip_start+20]
    ip_version = (ip_header[0] >> 4) & 0xF
    ip_ihl = (ip_header[0] & 0xF) * 4  # Longueur de l'en-tête IP en octets
    
    # Adresse IP source
    src_ip = '.'.join(str(b) for b in ip_header[12:16])
    dst_ip = '.'.join(str(b) for b in ip_header[16:20])
    
    # L'en-tête UDP commence après l'en-tête IP
    udp_start = ip_start + ip_ihl
    if udp_start + 8 > len(data):
        continue
    
    udp_header = data[udp_start:udp_start+8]
    src_port = int.from_bytes(udp_header[0:2], 'big')
    dst_port = int.from_bytes(udp_header[2:4], 'big')
    udp_len = int.from_bytes(udp_header[4:6], 'big')
    
    # Payload UDP
    payload_start = udp_start + 8
    payload_len = udp_len - 8
    payload = data[payload_start:payload_start+payload_len]
    
    packets.append({
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'src_port': src_port,
        'dst_port': dst_port,
        'payload': payload,
        'offset': start
    })

print(f"Nombre de paquets extraits: {len(packets)}")

# Afficher les premiers paquets
for i, p in enumerate(packets[:5]):
    print(f"Paquet {i}: src={p['src_ip']}:{p['src_port']} -> dst={p['dst_ip']}:{p['dst_port']}, payload={p['payload'][:20]}")