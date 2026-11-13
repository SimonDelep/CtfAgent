from scapy.all import *

# Lire le PCAP
packets = rdpcap('fenwick_capture.pcap')

# Filtrer les paquets TCP sur le port 8443
tcp_8443 = [p for p in packets if TCP in p and (p[TCP].dport == 8443 or p[TCP].sport == 8443)]

print(f"Nombre de paquets TCP sur 8443: {len(tcp_8443)}")

# Extraire les données TCP
for i, pkt in enumerate(tcp_8443[:20]):
    if TCP in pkt and Raw in pkt:
        payload = bytes(pkt[Raw].load)
        print(f"Paquet {i}: {pkt[IP].src}:{pkt[TCP].sport} -> {pkt[IP].dst}:{pkt[TCP].dport}, len={len(payload)}")
        print(f"  Payload (hex): {payload[:50].hex()}")
        print(f"  Payload (ascii): {payload[:50]}")
        print()