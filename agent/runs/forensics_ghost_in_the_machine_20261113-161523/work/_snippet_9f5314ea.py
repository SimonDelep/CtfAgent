import struct
from collections import defaultdict

with open('capture.pcap', 'rb') as f:
    f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) < 42:
            continue
        
        ip_start = 14
        ip_header = pkt_data[ip_start:ip_start+20]
        ip_ihl = (ip_header[0] & 0x0F) * 4
        
        udp_start = ip_start + ip_ihl
        if len(pkt_data) < udp_start + 8:
            continue
        udp_header = pkt_data[udp_start:udp_start+8]
        src_port, dst_port, udp_len, udp_checksum = struct.unpack('!HHHH', udp_header)
        
        packets.append({'ts': ts_sec * 1000000 + ts_usec, 'src_port': src_port})
    
    # Get first occurrence of each frequent port (400xx)
    freq_ports_400xx = [p for p in packets if 40000 <= p['src_port'] < 40200]
    
    # Get unique ports in order of first appearance
    seen = set()
    first_appearance = []
    for p in freq_ports_400xx:
        if p['src_port'] not in seen:
            seen.add(p['src_port'])
            first_appearance.append(p['src_port'])
    
    print("First appearance order of 400xx ports:", first_appearance)
    print("Values - 40000:", [p - 40000 for p in first_appearance])
    print("As chars:", ''.join(chr(p - 40000) for p in first_appearance))