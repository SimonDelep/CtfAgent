import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

offset = 24
paquets = []

while offset + 16 <= len(data):
    header = data[offset:offset+16]
    incl_len = struct.unpack('<I', header[8:12])[0]
    
    if incl_len == 0 or offset + 16 + incl_len > len(data):
        break
    
    packet_data = data[offset+16:offset+16+incl_len]
    
    # deadbeef 0002 deadbeef 0001 0800 (14 octets)
    ip_start = 14
    
    # IP header
    checksum_ip = struct.unpack('>H', packet_data[ip_start+10:ip_start+12])[0]
    src_ip = '.'.join(str(b) for b in packet_data[ip_start+12:ip_start+16])
    dst_ip = '.'.join(str(b) for b in packet_data[ip_start+16:ip_start+20])
    
    # UDP
    udp_start = ip_start + 20
    src_port = struct.unpack('>H', packet_data[udp_start:udp_start+2])[0]
    dst_port = struct.unpack('>H', packet_data[udp_start+2:udp_start+4])[0]
    
    # Champ avant IP (0800)
    champ_avant_ip = struct.unpack('>H', packet_data[12:14])[0]
    
    # Payload
    payload = packet_data[udp_start+8:]
    
    paquets.append({
        'champ_avant_ip': champ_avant_ip,
        'checksum_ip': checksum_ip,
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'src_port': src_port,
        'dst_port': dst_port,
        'payload': payload
    })
    
    offset += 16 + incl_len

print(f"Nombre de paquets: {len(paquets)}")

# Afficher les premiers paquets
for i, p in enumerate(paquets[:20]):
    print(f"Paquet {i}: champ={p['champ_avant_ip']:04x}, checksum_ip={p['checksum_ip']:04x}, src_port={p['src_port']}, dst_port={p['dst_port']}, payload={p['payload'].hex()}")
