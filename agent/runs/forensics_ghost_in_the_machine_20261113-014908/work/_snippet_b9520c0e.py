import struct

# Lire le pcap manuellement pour voir tous les champs
with open('capture.pcap', 'rb') as f:
    # Header pcap
    magic = f.read(4)
    version_major = struct.unpack('<H', f.read(2))[0]
    version_minor = struct.unpack('<H', f.read(2))[0]
    thiszone = struct.unpack('<i', f.read(4))[0]
    sigfigs = struct.unpack('<I', f.read(4))[0]
    snaplen = struct.unpack('<I', f.read(4))[0]
    network = struct.unpack('<I', f.read(4))[0]
    
    print(f"Magic: {magic.hex()}, Network: {network}")
    
    packets = []
    while True:
        ts_sec = f.read(4)
        if len(ts_sec) < 4:
            break
        ts_sec = struct.unpack('<I', ts_sec)[0]
        ts_usec = struct.unpack('<I', f.read(4))[0]
        incl_len = struct.unpack('<I', f.read(4))[0]
        orig_len = struct.unpack('<I', f.read(4))[0]
        
        data = f.read(incl_len)
        
        # Skip Ethernet header (14 bytes) + IP header (20 bytes) + UDP header (8 bytes)
        # Network = 1 = Ethernet
        if len(data) >= 42:  # 14 + 20 + 8 = 42
            eth = data[:14]
            ip = data[14:34]
            udp = data[34:42]
            payload = data[42:]
            
            # Parse IP header
            ip_version_ihl = ip[0]
            ip_header_len = (ip_version_ihl & 0x0F) * 4
            ip_total_len = struct.unpack('>H', ip[2:4])[0]
            ip_proto = ip[9]
            ip_src = '.'.join(str(b) for b in ip[12:16])
            ip_dst = '.'.join(str(b) for b in ip[16:20])
            
            # Parse UDP header
            udp_src_port = struct.unpack('>H', udp[0:2])[0]
            udp_dst_port = struct.unpack('>H', udp[2:4])[0]
            udp_len = struct.unpack('>H', udp[4:6])[0]
            udp_checksum = struct.unpack('>H', udp[6:8])[0]
            
            packets.append({
                'src_port': udp_src_port,
                'dst_port': udp_dst_port,
                'checksum': udp_checksum,
                'payload': payload.hex(),
                'ip_src': ip_src,
                'ip_dst': ip_dst
            })

print(f"Total packets: {len(packets)}")

# Regarder les ports source uniques
src_ports = sorted(set(p['src_port'] for p in packets))
print(f"Unique src_ports: {len(src_ports)}")
print(f"First 20 src_ports: {src_ports[:20]}")

# Regarder les checksums
checksums = set(p['checksum'] for p in packets)
print(f"Unique checksums: {checksums}")

# Regarder les payloads
payloads = set(p['payload'] for p in packets)
print(f"Unique payloads: {payloads}")
