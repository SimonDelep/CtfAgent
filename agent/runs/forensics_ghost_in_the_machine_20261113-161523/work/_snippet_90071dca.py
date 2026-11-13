# Re-lisons le pcap pour obtenir les ports fréquents
import struct
from collections import defaultdict

with open('capture.pcap', 'rb') as f:
    f.read(24)  # Skip pcap header
    
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
    
    # Count port frequencies
    port_counts = defaultdict(int)
    for p in packets:
        port_counts[p['src_port']] += 1
    
    # Find frequent ports (appearing more than once)
    frequent_ports = {port: count for port, count in port_counts.items() if count > 1}
    singleton_ports = {port for port, count in port_counts.items() if count == 1}
    
    print(f"Total unique ports: {len(port_counts)}")
    print(f"Frequent ports: {len(frequent_ports)}")
    print(f"Singleton ports: {len(singleton_ports)}")
    print()
    
    # Show frequent ports and their counts
    print("Frequent ports (port: count):")
    for port, count in sorted(frequent_ports.items())[:10]:
        print(f"  {port}: {count}")
    
    # Show what "sh4dow" would be if we subtract 40000
    print()
    print("Frequent ports - 40000:")
    for port in sorted(frequent_ports.keys())[:10]:
        print(f"  {port} - 40000 = {port - 40000} = '{chr(port - 40000)}'")
    
    # Get all frequent ports values
    freq_values = sorted(frequent_ports.keys())
    print()
    print("All frequent ports:", freq_values)
    print("Frequent ports - 40000:", [p - 40000 for p in freq_values])