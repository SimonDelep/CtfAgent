# Extraction des ports sources et payloads
import struct

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

# Chaque paquet: deadbeef (4) + 2 octets + deadbeef (4) + 4 octets méta + IP (20) + UDP (8) + payload
# Donc offset IP = position du 2ème deadbeef + 4 + 4 = position + 8 + 4 = position + 12
# Mais attention: positions[i] est le 1er deadbeef, positions[i+1] est le 2ème deadbeef

packets_info = []
for i in range(0, len(positions), 2):
    first_deadbeef = positions[i]
    second_deadbeef = positions[i+1]
    
    # Entre les deux deadbeef: 2 octets
    # Après le 2ème deadbeef: 4 octets méta, puis IP header
    offset_ip = second_deadbeef + 4 + 4  # 4 (deadbeef) + 4 (méta)
    
    # IP header: 20 octets minimum
    # Port source est à offset 20:22 dans l'IP header
    ip_header = data[offset_ip:offset_ip+20]
    
    if len(ip_header) >= 22:
        src_port = struct.unpack('>H', ip_header[20:22])[0]
        dst_port = struct.unpack('>H', ip_header[22:24])[0]
        
        # Payload UDP: après IP header (20) + UDP header (8) = 28 octets depuis offset_ip
        udp_start = offset_ip + 20
        udp_header = data[udp_start:udp_start+8]
        udp_len = struct.unpack('>H', udp_header[4:6])[0]
        payload_len = udp_len - 8
        
        payload = data[udp_start+8:udp_start+8+payload_len]
        
        packets_info.append({
            'src_port': src_port,
            'dst_port': dst_port,
            'payload': payload,
            'offset_ip': offset_ip
        })

print(f"Nombre de paquets extraits: {len(packets_info)}")

# Afficher quelques exemples
for i, p in enumerate(packets_info[:5]):
    print(f"Paquet {i}: src_port={p['src_port']}, dst_port={p['dst_port']}, payload={p['payload'][:20]}")