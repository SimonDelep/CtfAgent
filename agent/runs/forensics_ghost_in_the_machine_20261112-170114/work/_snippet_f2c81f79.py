import struct

# Lecture complète du PCAP pour analyser tous les paquets
with open('capture.pcap', 'rb') as f:
    # En-tête PCAP global
    magic = struct.unpack('<I', f.read(4))[0]
    version_major, version_minor = struct.unpack('<HH', f.read(4))
    thiszone, sigfigs, snaplen = struct.unpack('<III', f.read(12))
    network = struct.unpack('<I', f.read(4))[0]
    
    packets = []
    while True:
        header = f.read(16)
        if len(header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', header)
        packet = f.read(incl_len)
        packets.append((ts_sec, ts_usec, packet))
    
    print(f"Total packets: {len(packets)}")
    
    # Analysons les paquets UDP
    udp_packets = []
    for i, (ts_sec, ts_usec, packet) in enumerate(packets):
        if len(packet) >= 14:
            eth_type = struct.unpack('>H', packet[12:14])[0]
            if eth_type == 0x0800:  # IPv4
                ip = packet[14:]
                ip_ihl = (ip[0] & 0xF) * 4
                ip_proto = ip[9]
                
                if ip_proto == 17:  # UDP
                    udp_start = 14 + ip_ihl
                    udp = packet[udp_start:]
                    if len(udp) >= 8:
                        src_port = struct.unpack('>H', udp[0:2])[0]
                        dst_port = struct.unpack('>H', udp[2:4])[0]
                        udp_len = struct.unpack('>H', udp[4:6])[0]
                        payload = udp[8:]
                        udp_packets.append({
                            'idx': i,
                            'ts': ts_sec + ts_usec/1000000,
                            'src_port': src_port,
                            'dst_port': dst_port,
                            'payload': payload,
                            'packet': packet
                        })
    
    print(f"UDP packets: {len(udp_packets)}")
    
    # Affichons les premiers paquets UDP
    for p in udp_packets[:20]:
        print(f"\nPacket {p['idx']}: src_port={p['src_port']}, dst_port={p['dst_port']}, payload_len={len(p['payload'])}")
        print(f"  Payload hex: {p['payload'][:40].hex()}")
        # Tentative de lecture ASCII
        try:
            ascii_data = p['payload'].decode('ascii', errors='replace')
            print(f"  ASCII: {ascii_data[:50]}")
        except:
            pass
