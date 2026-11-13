import dpkt

pcap_path = "/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/misc_keep_walking_forward_20261112-174941/work/capture.pcapng"

# Lire le pcapng
with open(pcap_path, 'rb') as f:
    reader = dpkt.pcapng.Reader(f)
    
    count = 0
    for ts, buf in reader:
        count += 1
        if count <= 5:
            eth = dpkt.ethernet.Ethernet(buf)
            print(f"Paquet {count}: {eth.__class__.__name__}")
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                print(f"  IP: {ip.src} -> {ip.dst}")
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    print(f"  TCP: {tcp.sport} -> {tcp.dport}")
                    if len(tcp.data) > 0:
                        print(f"  Data len: {len(tcp.data)}")
                        print(f"  Data hex: {tcp.data[:50].hex()}")