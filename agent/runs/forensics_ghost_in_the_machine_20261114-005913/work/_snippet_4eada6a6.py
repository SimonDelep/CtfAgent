# Examiner les payloads
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

packets = []
for i in range(0, len(positions), 2):
    start = positions[i]
    ip_start = start + 14
    
    if ip_start + 28 > len(data):
        continue
    
    ip_header = data[ip_start:ip_start+20]
    ip_ihl = (ip_header[0] & 0xF) * 4
    src_ip = '.'.join(str(b) for b in ip_header[12:16])
    dst_ip = '.'.join(str(b) for b in ip_header[16:20])
    
    udp_start = ip_start + ip_ihl
    if udp_start + 8 > len(data):
        continue
    
    udp_header = data[udp_start:udp_start+8]
    src_port = int.from_bytes(udp_header[0:2], 'big')
    dst_port = int.from_bytes(udp_header[2:4], 'big')
    udp_len = int.from_bytes(udp_header[4:6], 'big')
    
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

# Afficher les payloads uniques
payloads = [p['payload'] for p in packets]
unique_payloads = set(payloads)
print(f"Nombre de payloads uniques: {len(unique_payloads)}")

# Afficher quelques payloads
for i, p in enumerate(packets[:10]):
    print(f"Paquet {i}: src_port={p['src_port']}, payload={p['payload'][:30]}")

# Vérifier si tous les payloads commencent par "PING"
ping_count = sum(1 for p in packets if p['payload'][:4] == b'PING')
print(f"\nPaquets avec 'PING' en début: {ping_count}/{len(packets)}")