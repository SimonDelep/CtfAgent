import struct

with open("capture.pcapng", 'rb') as f:
    data = f.read()

pos = 24  # Après header global

packets = []
packet_num = 0

while pos + 16 <= len(data):
    ts_sec = struct.unpack('<I', data[pos:pos+4])[0]
    ts_usec = struct.unpack('<I', data[pos+4:pos+8])[0]
    incl_len = struct.unpack('<I', data[pos+8:pos+12])[0]
    orig_len = struct.unpack('<I', data[pos+12:pos+16])[0]
    
    # Vérifier si c'est un paquet valide
    if incl_len == 0 or incl_len > 65535:
        print(f"Paquet {packet_num} à pos={pos}: incl_len={incl_len} semble invalide, arrêtons")
        break
    
    if pos + 16 + incl_len > len(data):
        print(f"Paquet {packet_num} à pos={pos}: incl_len={incl_len} dépasse la fin du fichier")
        break
    
    pkt_data = data[pos+16:pos+16+incl_len]
    packets.append((ts_sec, ts_usec, pkt_data, incl_len, orig_len))
    
    # Calculer le padding
    padding = (4 - (incl_len % 4)) % 4
    next_pos = pos + 16 + incl_len + padding
    
    print(f"Paquet {packet_num}: ts={ts_sec}.{ts_usec}, incl_len={incl_len}, orig_len={orig_len}, padding={padding}, next_pos={next_pos}")
    
    pos = next_pos
    packet_num += 1
    
    if packet_num > 100:  # Sécurité
        break

print(f"\nTotal paquets: {len(packets)}")

# Analyser les paquets
for i, (ts_sec, ts_usec, pkt, incl_len, orig_len) in enumerate(packets):
    if len(pkt) < 14:
        continue
    
    ethertype = struct.unpack('>H', pkt[12:14])[0]
    
    if ethertype == 0x0800:  # IP
        ip_start = 14
        if len(pkt) < ip_start + 20:
            continue
        ip_header = pkt[ip_start:ip_start+20]
        
        if ip_header[0] != 0x45:
            continue
            
        ihl = (ip_header[0] & 0x0F) * 4
        protocol = ip_header[9]
        src_ip = '.'.join(str(b) for b in ip_header[12:16])
        dst_ip = '.'.join(str(b) for b in ip_header[16:20])
        
        if protocol == 6:  # TCP
            tcp_start = ip_start + ihl
            if len(pkt) < tcp_start + 20:
                continue
            tcp_header = pkt[tcp_start:tcp_start+20]
            src_port = struct.unpack('>H', tcp_header[0:2])[0]
            dst_port = struct.unpack('>H', tcp_header[2:4])[0]
            data_offset = (tcp_header[12] >> 4) * 4
            tcp_data = pkt[tcp_start+data_offset:]
            
            if len(tcp_data) > 0:
                print(f"Paquet {i}: {src_ip}:{src_port} -> {dst_ip}:{dst_port}, len={len(tcp_data)}")
                if src_port == 443 or dst_port == 443:
                    content_type = tcp_data[0]
                    print(f"  -> TLS type={content_type}")
                    if content_type == 23:
                        print(f"  -> App Data: {tcp_data[:100].hex()}")
    elif ethertype == 0x0806:  # ARP
        print(f"Paquet {i}: ARP")
