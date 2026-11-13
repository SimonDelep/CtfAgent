import struct

pcap_file = "capture.pcap"

with open(pcap_file, "rb") as f:
    magic = f.read(4)
    print(f"Magic: {magic.hex()}")
    
    if magic == b'\xa1\xb2\xc3\xd4':
        endian = '<'
    elif magic == b'\xd4\xc3\xb2\xa1':
        endian = '>'
    else:
        print(f"Magic inconnu: {magic.hex()}")
        endian = '<'
    
    header = f.read(24)
    version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack(endian + 'HHIIHH', header)
    print(f"Version: {version_major}.{version_minor}, Network: {network}")
    
    packets = []
    count = 0
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) < incl_len:
            break
        
        # Ethernet header (14 bytes)
        eth_len = 14
        if len(pkt_data) < eth_len + 28:
            continue
        
        ip_start = eth_len
        ip_header = pkt_data[ip_start:ip_start+20]
        if len(ip_header) < 20:
            continue
        
        version_ihl = ip_header[0]
        ihl = (version_ihl & 0x0F) * 4
        protocol = ip_header[9]
        
        if protocol != 17:  # UDP
            continue
        
        udp_start = ip_start + ihl
        udp_header = pkt_data[udp_start:udp_start+8]
        if len(udp_header) < 8:
            continue
        
        src_port, dst_port, length, checksum = struct.unpack('>HHHH', udp_header)
        
        packets.append({
            'ts': ts_sec + ts_usec / 1000000.0,
            'src_port': src_port,
            'dst_port': dst_port,
            'length': length
        })
        count += 1
        if count <= 5:
            print(f"Packet {count}: src_port={src_port}, dst_port={dst_port}, length={length}")
    
    print(f"Total paquets UDP: {len(packets)}")
    
    # Compter les occurrences de chaque port source
    port_counts = {}
    for pkt in packets:
        port = pkt['src_port']
        port_counts[port] = port_counts.get(port, 0) + 1
    
    # Identifier les singletons
    singleton_ports = {port for port, count in port_counts.items() if count == 1}
    frequent_ports = {port for port, count in port_counts.items() if count > 1}
    
    print(f"Ports singletons: {len(singleton_ports)}")
    print(f"Ports fréquents: {len(frequent_ports)}")
    print(f"Top ports fréquents: {sorted(port_counts.items(), key=lambda x: -x[1])[:10]}")