import dpkt

with open("capture.pcap", "rb") as f:
    pcap = dpkt.pcap.Reader(f)
    
    # Extraire les 20 premiers paquets UDP
    count = 0
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if isinstance(eth.data, dpkt.ip.IP):
            ip = eth.data
            if isinstance(ip.data, dpkt.udp.UDP):
                udp = ip.data
                payload = bytes(udp.data)
                print(f"src_port={udp.sport} dst_port={udp.dport} payload={payload.hex()} ip_id={ip.id} ttl={ip.ttl} checksum={udp.chksum}")
                count += 1
                if count >= 20:
                    break