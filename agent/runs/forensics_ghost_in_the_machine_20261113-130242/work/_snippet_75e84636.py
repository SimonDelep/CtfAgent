import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Analyser tous les paquets
offset = 24  # après header PCAP
paquets = []

while offset + 16 <= len(data):
    # Header du paquet PCAP
    header = data[offset:offset+16]
    ts_sec = struct.unpack('<I', header[0:4])[0]
    ts_usec = struct.unpack('<I', header[4:8])[0]
    incl_len = struct.unpack('<I', header[8:12])[0]
    orig_len = struct.unpack('<I', header[12:16])[0]
    
    if incl_len == 0 or offset + 16 + incl_len > len(data):
        break
    
    # Données du paquet
    packet_data = data[offset+16:offset+16+incl_len]
    
    # Vérifier le format deadbeef
    if packet_data[:4] != b'\xde\xad\xbe\xef':
        print(f"Paquet à offset {offset} n'a pas deadbeef: {packet_data[:10].hex()}")
        break
    
    # deadbeef 0002 deadbeef 0001
    if packet_data[4:6] != b'\x00\x02' or packet_data[6:10] != b'\xde\xad\xbe\xef' or packet_data[10:12] != b'\x00\x01':
        print(f"Format inattendu à offset {offset}: {packet_data[:15].hex()}")
    
    # Après deadbeef 0001 (offset 12), on a l'en-tête IP
    ip_start = 12
    ip_header = packet_data[ip_start:ip_start+20]
    
    # Version/IHL
    ver_ihl = ip_header[0]
    ihl = (ver_ihl & 0xF) * 4
    
    # Longueur totale IP
    total_len = struct.unpack('>H', ip_header[2:4])[0]
    
    # TTL, protocole
    ttl = ip_header[8]
    protocol = ip_header[9]
    
    # Checksum IP
    checksum_ip = struct.unpack('>H', ip_header[10:12])[0]
    
    # Adresses IP
    src_ip = '.'.join(str(b) for b in ip_header[12:16])
    dst_ip = '.'.join(str(b) for b in ip_header[16:20])
    
    # UDP start
    udp_start = ip_start + ihl
    udp_header = packet_data[udp_start:udp_start+8]
    
    src_port = struct.unpack('>H', udp_header[0:2])[0]
    dst_port = struct.unpack('>H', udp_header[2:4])[0]
    udp_len = struct.unpack('>H', udp_header[4:6])[0]
    udp_checksum = struct.unpack('>H', udp_header[6:8])[0]
    
    # Payload UDP
    payload_start = udp_start + 8
    payload = packet_data[payload_start:payload_start+udp_len-8] if udp_len > 8 else b''
    
    paquets.append({
        'ts_sec': ts_sec,
        'ts_usec': ts_usec,
        'checksum_ip': checksum_ip,
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'src_port': src_port,
        'dst_port': dst_port,
        'udp_len': udp_len,
        'payload': payload
    })
    
    offset += 16 + incl_len

print(f"Nombre de paquets: {len(paquets)}")

# Afficher les premiers paquets
for i, p in enumerate(paquets[:10]):
    print(f"Paquet {i}: checksum_ip={p['checksum_ip']:04x}, src_port={p['src_port']}, dst_port={p['dst_port']}, payload={p['payload'].hex()}")
