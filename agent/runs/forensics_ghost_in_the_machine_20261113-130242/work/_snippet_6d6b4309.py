import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Parser tous les paquets en cherchant le pattern deadbeef 0001
offset = 24  # après le header PCAP
paquets = []

while offset < len(data) - 20:
    # Chercher deadbeef 0001
    idx = data.find(b'\xde\xad\xbe\xef\x00\x01', offset)
    if idx == -1:
        break
    
    # À partir de idx+6, on devrait avoir l'en-tête IP
    # deadbeef 0001 0800 4500 ...
    ip_start = idx + 6  # après deadbeef 0001 0800
    
    if ip_start + 20 > len(data):
        break
    
    # Lire l'en-tête IP (20 octets)
    ip_header = data[ip_start:ip_start+20]
    
    # Version/IHL
    ver_ihl = ip_header[0]
    version = (ver_ihl >> 4) & 0xF
    ihl = (ver_ihl & 0xF) * 4
    
    # Longueur totale
    total_len = struct.unpack('>H', ip_header[2:4])[0]
    
    # TTL, protocole
    ttl = ip_header[8]
    protocol = ip_header[9]
    
    # Checksum IP
    checksum_ip = struct.unpack('>H', ip_header[10:12])[0]
    
    # Adresses IP
    src_ip = '.'.join(str(b) for b in ip_header[12:16])
    dst_ip = '.'.join(str(b) for b in ip_header[16:20])
    
    # Données UDP commencent après l'en-tête IP
    udp_start = ip_start + ihl
    
    # En-tête UDP (8 octets)
    if udp_start + 8 <= len(data):
        udp_header = data[udp_start:udp_start+8]
        src_port = struct.unpack('>H', udp_header[0:2])[0]
        dst_port = struct.unpack('>H', udp_header[2:4])[0]
        udp_len = struct.unpack('>H', udp_header[4:6])[0]
        udp_checksum = struct.unpack('>H', udp_header[6:8])[0]
        
        # Payload UDP
        payload_start = udp_start + 8
        payload_len = udp_len - 8
        payload = data[payload_start:payload_start+payload_len] if payload_len > 0 else b''
        
        paquets.append({
            'offset': idx,
            'checksum_ip': checksum_ip,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'payload': payload,
            'total_len': total_len
        })
    
    offset = idx + 1  # continuer la recherche

print(f"Nombre de paquets extraits: {len(paquets)}")

# Afficher les premiers paquets
for i, p in enumerate(paquets[:5]):
    print(f"Paquet {i}: checksum_ip={p['checksum_ip']:04x}, src_port={p['src_port']}, dst_port={p['dst_port']}, payload={p['payload'][:30].hex()}")
