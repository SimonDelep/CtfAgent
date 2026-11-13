# Parse le pcapng manuellement pour extraire les paquets TCP
import struct

def read_pcapng(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    packets = []
    pos = 0
    
    # Skip Section Header Block (SHB)
    if struct.unpack('<I', data[pos:pos+4])[0] == 0x0A0D0D0A:  # Section Header Block
        shb_len = struct.unpack('<I', data[pos+12:pos+16])[0]
        pos += shb_len
        if shb_len % 8 != 0:
            pos += 8 - (shb_len % 8)
    
    while pos < len(data):
        block_type = struct.unpack('<I', data[pos:pos+4])[0]
        block_len = struct.unpack('<I', data[pos+4:pos+8])[0]
        
        if block_type == 6:  # Interface Description Block
            pos += block_len
            if block_len % 8 != 0:
                pos += 8 - (block_len % 8)
        elif block_type == 7:  # Simple Packet Block
            # Format: block_type(4) + total_len(4) + packet_data + padding + block_len(4)
            packet_data_len = block_len - 16  # 4 (type) + 4 (len) + 4 (total_len) + padding
            packet_data = data[pos+8:pos+8+packet_data_len]
            packets.append(packet_data)
            pos += block_len
            if block_len % 8 != 0:
                pos += 8 - (block_len % 8)
        elif block_type == 8:  # Enhanced Packet Block
            # Enhanced Packet Block: type(4) + len(4) + interface_id(4) + timestamp(8) + cap_len(4) + orig_len(4) + data + padding + len(4)
            interface_id = struct.unpack('<I', data[pos+8:pos+12])[0]
            timestamp = struct.unpack('<Q', data[pos+12:pos+20])[0]
            cap_len = struct.unpack('<I', data[pos+20:pos+24])[0]
            orig_len = struct.unpack('<I', data[pos+24:pos+28])[0]
            packet_data = data[pos+28:pos+28+cap_len]
            packets.append(packet_data)
            pos += block_len
            if block_len % 8 != 0:
                pos += 8 - (block_len % 8)
        elif block_type == 0x00000001:  # End of Section
            break
        else:
            # Skip unknown block
            pos += block_len
            if block_len % 8 != 0:
                pos += 8 - (block_len % 8)
    
    return packets

packets = read_pcapng("capture.pcapng")
print(f"Nombre de paquets: {len(packets)}")

# Analyser chaque paquet
for i, pkt in enumerate(packets):
    if len(pkt) < 20:
        continue
    
    # Vérifier si c'est IP (Ethernet ou IP direct)
    # Dans pcapng, le lien peut être Ethernet (type 1) ou IP (type 227)
    # Essayons de détecter le type de lien
    
    # Si le premier octet est 0x45, c'est probablement IP direct (version 4, IHL 5)
    if pkt[0] == 0x45:
        # IP header
        ip_header = pkt[:20]
        version_ihl = ip_header[0]
        ihl = (version_ihl & 0x0F) * 4
        protocol = ip_header[9]
        src_ip = '.'.join(str(b) for b in ip_header[12:16])
        dst_ip = '.'.join(str(b) for b in ip_header[16:20])
        
        if protocol == 6:  # TCP
            tcp_header = pkt[20:20+20]
            src_port = struct.unpack('>H', tcp_header[0:2])[0]
            dst_port = struct.unpack('>H', tcp_header[2:4])[0]
            data_offset = (tcp_header[12] >> 4) * 4
            tcp_data = pkt[20+data_offset:]
            
            if len(tcp_data) > 0:
                # Vérifier si c'est du TLS (port 443)
                if src_port == 443 or dst_port == 443:
                    content_type = tcp_data[0] if len(tcp_data) > 0 else 0
                    print(f"Paquet {i}: {src_ip}:{src_port} -> {dst_ip}:{dst_port}, TLS type={content_type}, len={len(tcp_data)}")
                    if content_type == 22:
                        print(f"  -> Handshake")
                    elif content_type == 23:
                        print(f"  -> Application Data")
                    elif content_type == 16:
                        print(f"  -> Change Cipher Spec")
                    elif content_type == 20:
                        print(f"  -> Alert")
                    else:
                        print(f"  -> Données: {tcp_data[:50].hex()}")
    elif len(pkt) > 14:
        # Peut-être Ethernet
        eth_type = struct.unpack('>H', pkt[12:14])[0]
        if eth_type == 0x0800:  # IP
            ip_start = 14
            ip_header = pkt[ip_start:ip_start+20]
            if len(ip_header) >= 20 and ip_header[0] == 0x45:
                ihl = (ip_header[0] & 0x0F) * 4
                protocol = ip_header[9]
                src_ip = '.'.join(str(b) for b in ip_header[12:16])
                dst_ip = '.'.join(str(b) for b in ip_header[16:20])
                
                if protocol == 6:  # TCP
                    tcp_start = ip_start + ihl
                    tcp_header = pkt[tcp_start:tcp_start+20]
                    src_port = struct.unpack('>H', tcp_header[0:2])[0]
                    dst_port = struct.unpack('>H', tcp_header[2:4])[0]
                    data_offset = (tcp_header[12] >> 4) * 4
                    tcp_data = pkt[tcp_start+data_offset:]
                    
                    if len(tcp_data) > 0 and (src_port == 443 or dst_port == 443):
                        content_type = tcp_data[0] if len(tcp_data) > 0 else 0
                        print(f"Paquet {i}: {src_ip}:{src_port} -> {dst_ip}:{dst_port}, TLS type={content_type}, len={len(tcp_data)}")
