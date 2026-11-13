import struct

pcap_file = "capture.pcap"

with open(pcap_file, "rb") as f:
    magic = f.read(4)
    endian = '<'  # little-endian
    
    header = f.read(20)
    version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack(endian + 'HHIIII', header)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) < incl_len:
            break
        
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
        
        if protocol != 17:
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
    
    # Compter les occurrences de chaque port source
    port_counts = {}
    for pkt in packets:
        port = pkt['src_port']
        port_counts[port] = port_counts.get(port, 0) + 1
    
    # Identifier les singletons
    singleton_ports = {port for port, count in port_counts.items() if count == 1}
    
    # Extraire les paquets avec des ports singletons, triés par timestamp
    singleton_packets = [pkt for pkt in packets if pkt['src_port'] in singleton_ports]
    singleton_packets.sort(key=lambda x: x['ts'])
    
    # Afficher la séquence des ports singletons
    seq = [pkt['src_port'] for pkt in singleton_packets]
    print(f"Nombre de singletons: {len(seq)}")
    print(f"Séquence des ports singletons: {seq}")
    
    # Essayer de décoder
    # Option 1: port - 0xC000
    decoded1 = ''.join(chr(p - 0xC000) if 0 <= p - 0xC000 < 128 else '?' for p in seq)
    print(f"Décodage (port - 0xC000): {decoded1}")
    
    # Option 2: port - 0xC100
    decoded2 = ''.join(chr(p - 0xC100) if 0 <= p - 0xC100 < 128 else '?' for p in seq)
    print(f"Décodage (port - 0xC100): {decoded2}")
    
    # Option 3: port & 0xFF
    decoded3 = ''.join(chr(p & 0xFF) if 32 <= (p & 0xFF) < 127 else '.' for p in seq)
    print(f"Décodage (port & 0xFF): {decoded3}")
    
    # Option 4: port >> 8
    decoded4 = ''.join(chr(p >> 8) if 32 <= (p >> 8) < 127 else '.' for p in seq)
    print(f"Décodage (port >> 8): {decoded4}")