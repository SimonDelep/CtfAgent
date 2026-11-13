import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 12:
            val1 = struct.unpack('>H', pkt_data[4:6])[0]
            val2 = struct.unpack('>H', pkt_data[10:12])[0]
            payload = pkt_data[12:]
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'val1': val1,
                'val2': val2,
                'payload': payload
            })

# Le payload commence par 0800 (Ethernet type) puis header IP
# Analysons le header IP
# Offset 0-1: 0800 (Ethernet type)
# Offset 2-1: IP header (20 bytes minimum)
#   - Version/IHL: byte 2
#   - TOS: byte 3
#   - Total Length: bytes 4-5
#   - ID: bytes 6-7
#   - Flags/Fragment: bytes 8-9
#   - TTL: byte 10
#   - Protocol: byte 11
#   - Checksum: bytes 12-13
#   - Source IP: bytes 14-17
#   - Dest IP: bytes 18-21

# Regardons les variations dans le header IP
# Le payload est: 0800 + IP header + données

# Extraire les champs qui pourraient varier
variations = []
for i, p in enumerate(packets):
    payload = p['payload']
    if len(payload) >= 22:  # 2 bytes Ethernet + 20 bytes IP
        # IP header commence à offset 2
        ip_header = payload[2:22]
        
        # ID (bytes 6-7 de l'IP header, donc offset 8-9 du payload)
        ip_id = struct.unpack('>H', payload[8:10])[0]
        
        # TTL (byte 10 de l'IP header, donc offset 12 du payload)
        ttl = payload[12]
        
        # Checksum IP (bytes 12-13 de l'IP header, donc offset 14-15 du payload)
        ip_checksum = struct.unpack('>H', payload[14:16])[0]
        
        # Source IP (bytes 14-17 de l'IP header, donc offset 16-19 du payload)
        src_ip = payload[16:20]
        
        # Dest IP (bytes 18-21 de l'IP header, donc offset 20-23 du payload)
        dst_ip = payload[20:24]
        
        variations.append({
            'idx': i,
            'ts_usec': p['ts_usec'],
            'ip_id': ip_id,
            'ttl': ttl,
            'ip_checksum': ip_checksum,
            'src_ip': src_ip.hex(),
            'dst_ip': dst_ip.hex()
        })

# Regardons les valeurs uniques
print("Valeurs uniques de IP ID:", sorted(set(v['ip_id'] for v in variations)))
print("Valeurs uniques de TTL:", sorted(set(v['ttl'] for v in variations)))
print("Valeurs uniques de IP checksum:", sorted(set(v['ip_checksum'] for v in variations)))

# Compter les occurrences de chaque IP ID
ip_id_counts = Counter(v['ip_id'] for v in variations)
print(f"\nComptage IP ID: {dict(ip_id_counts)}")
