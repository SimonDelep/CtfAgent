from scapy.all import rdpcap, TCP, UDP, IP, Raw

packets = rdpcap('fenwick_capture.pcap')

# Extraire toutes les données TCP avec payload
for pkt in packets:
    if TCP in pkt and Raw in pkt:
        payload = bytes(pkt[Raw].load)
        src = pkt[IP].src
        dst = pkt[IP].dst
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        # Afficher les premiers octets
        if len(payload) > 0:
            print(f"{src}:{sport} -> {dst}:{dport} ({len(payload)} bytes)")
            print(f"  {payload[:100]}")
            print()