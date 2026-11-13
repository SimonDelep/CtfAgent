from scapy.all import rdpcap, UDP, IP

packets = rdpcap("capture.pcap")

# Extraire toutes les informations pertinentes de chaque paquet
data = []
for i, pkt in enumerate(packets):
    if UDP in pkt:
        udp = pkt[UDP]
        ip = pkt[IP] if IP in pkt else None
        
        row = {
            'idx': i,
            'src_port': udp.sport,
            'dst_port': udp.dport,
            'payload': bytes(udp.payload).hex() if udp.payload else "",
            'ip_id': ip.id if ip else None,
            'ip_ttl': ip.ttl if ip else None,
            'ip_src': ip.src if ip else None,
            'ip_dst': ip.dst if ip else None,
            'udp_checksum': udp.chksum if udp else None,
            'time': float(pkt.time)
        }
        data.append(row)

# Afficher les 20 premiers paquets
for d in data[:20]:
    print(d)