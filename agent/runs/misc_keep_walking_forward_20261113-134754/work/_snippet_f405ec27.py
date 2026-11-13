import struct

def read_pcap(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Pcap global header
    magic = struct.unpack('<I', data[0:4])[0]
    version_major = struct.unpack('<H', data[4:6])[0]
    version_minor = struct.unpack('<H', data[6:8])[0]
    snaplen = struct.unpack('<I', data[16:20])[0]
    network = struct.unpack('<I', data[20:24])[0]
    
    packets = []
    pos = 24  # Après le header global
    
    while pos + 16 <= len(data):
        # Packet header: ts_sec(4) + ts_usec(4) + incl_len(4) + orig_len(4)
        ts_sec = struct.unpack('<I', data[pos:pos+4])[0]
        ts_usec = struct.unpack('<I', data[pos+4:pos+8])[0]
        incl_len = struct.unpack('<I', data[pos+8:pos+12])[0]
        orig_len = struct.unpack('<I', data[pos+12:pos+16])[0]
        
        if incl_len == 0 or incl_len > snaplen:
            break
            
        if pos + 16 + incl_len > len(data):
            break
            
        packet_data = data[pos+16:pos+16+incl_len]
        packets.append((ts_sec, ts_usec, packet_data, incl_len, orig_len))
        
        # Avancer au prochain paquet
        pos += 16 + incl_len
        # Alignement pcap: les paquets sont alignés sur 4 octets
        if incl_len % 4 != 0:
            pos += 4 - (incl_len % 4)
    
    return packets

packets = read_pcap("capture.pcapng")
print(f"Nombre de paquets: {len(packets)}")

# Analyser chaque paquet
tcp_flows = {}
for i, (ts_sec, ts_usec, pkt, incl_len, orig_len) in enumerate(packets):
    if len(pkt) < 14:
        continue
    
    # Ethernet header
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
            seq = struct.unpack('>I', tcp_header[4:8])[0]
            ack = struct.unpack('>I', tcp_header[8:12])[0]
            flags = tcp_header[13]
            data_offset = (tcp_header[12] >> 4) * 4
            tcp_data = pkt[tcp_start+data_offset:]
            
            # Identifier le flux
            flow_key = tuple(sorted([(src_ip, src_port), (dst_ip, dst_port)]))
            if flow_key not in tcp_flows:
                tcp_flows[flow_key] = []
            tcp_flows[flow_key].append((src_port, dst_port, tcp_data, seq, flags))
            
            if len(tcp_data) > 0:
                print(f"Paquet {i}: {src_ip}:{src_port} -> {dst_ip}:{dst_port}, len={len(tcp_data)}, flags={flags:02x}")
                if src_port == 443 or dst_port == 443:
                    content_type = tcp_data[0] if len(tcp_data) > 0 else 0
                    print(f"  -> TLS type={content_type}")
                    if content_type == 23:  # Application Data
                        print(f"  -> App Data: {tcp_data[:80].hex()}")
    elif ethertype == 0x0806:  # ARP
        print(f"Paquet {i}: ARP")

print(f"\nFlux TCP trouvés: {len(tcp_flows)}")
for flow_key, pkts in tcp_flows.items():
    print(f"  Flux: {flow_key}, {len(pkts)} paquets")
