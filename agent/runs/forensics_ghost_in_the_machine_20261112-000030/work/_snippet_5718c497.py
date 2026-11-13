import struct

# Re-lisons le pcap
with open('capture.pcap', 'rb') as f:
    data = f.read()

offset = 24
packets = []
while offset < len(data):
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append(pkt_data)

# Analysons la structure IP/UDP de plusieurs paquets
print("Analyse des champs IP/UDP:")
print("=" * 60)

for i in range(min(10, len(packets))):
    pkt = packets[i]
    # Skip Ethernet header (14 bytes)
    eth_header = pkt[:14]
    # IP header starts at offset 14
    ip_header = pkt[14:34]
    
    # IP header structure:
    # Version/IHL (1), TOS (1), Total Length (2), ID (2), Flags/Fragment (2), TTL (1), Protocol (1), Checksum (2), Src IP (4), Dst IP (4)
    
    version_ihl = ip_header[0]
    ip_version = version_ihl >> 4
    ip_ihl = version_ihl & 0x0F
    ip_total_len = struct.unpack('>H', ip_header[2:4])[0]
    ip_id = struct.unpack('>H', ip_header[4:6])[0]
    flags_frag = struct.unpack('>H', ip_header[6:8])[0]
    ttl = ip_header[8]
    protocol = ip_header[9]
    ip_checksum = struct.unpack('>H', ip_header[10:12])[0]
    src_ip = '.'.join(str(b) for b in ip_header[12:16])
    dst_ip = '.'.join(str(b) for b in ip_header[16:20])
    
    # UDP header starts after IP header
    udp_start = 14 + 20  # Ethernet(14) + IP(20)
    udp_header = pkt[udp_start:udp_start+8]
    udp_src_port = struct.unpack('>H', udp_header[0:2])[0]
    udp_dst_port = struct.unpack('>H', udp_header[2:4])[0]
    udp_len = struct.unpack('>H', udp_header[4:6])[0]
    udp_checksum = struct.unpack('>H', udp_header[6:8])[0]
    
    print(f"Packet {i}:")
    print(f"  IP ID: {ip_id:04x}, TTL: {ttl}, Flags/Frag: {flags_frag:04x}")
    print(f"  UDP ports: {udp_src_port} -> {udp_dst_port}, len: {udp_len}")
    print(f"  Payload: {pkt[udp_start+8:]}")
    print()