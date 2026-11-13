import sys
sys.path.insert(0, './scapy_lib')
from scapy.all import *

# Lire le PCAP
packets = rdpcap('capture.pcapng')

# Extraire les paquets TCP avec données Raw sur le port 443
tcp_packets = []
for p in packets:
    if TCP in p and p.haslayer(Raw):
        if p[TCP].dport == 443 or p[TCP].sport == 443:
            tcp_packets.append(p)

print(f"Paquets TCP avec Raw sur port 443: {len(tcp_packets)}")

# Afficher les données Raw
for i, p in enumerate(tcp_packets):
    raw_data = bytes(p[Raw].load)
    src = f"{p[IP].src}:{p[TCP].sport}"
    dst = f"{p[IP].dst}:{p[TCP].dport}"
    print(f"Paquet {i}: {src} -> {dst}, len={len(raw_data)}, first_bytes={raw_data[:20].hex()}")