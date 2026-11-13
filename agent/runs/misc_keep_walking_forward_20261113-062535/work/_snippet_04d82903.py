import sys
sys.path.insert(0, '/home/etudiantelambda/.local/lib/python3.12/site-packages')
from scapy.all import *

# Lire le pcapng
packets = rdpcap("capture.pcapng")

print(f"Nombre total de paquets: {len(packets)}")

# Regarder les ports
from collections import Counter
ports = Counter()
for p in packets:
    if p.haslayer(TCP):
        ports[(p[TCP].sport, p[TCP].dport)] += 1

print(f"Ports TCP (sport, dport): {dict(ports)}")

# Afficher quelques paquets
for i, p in enumerate(packets[:5]):
    print(f"\n--- Paquet {i} ---")
    if p.haslayer(IP):
        print(f"IP: {p[IP].src} -> {p[IP].dst}")
    if p.haslayer(TCP):
        print(f"TCP: {p[TCP].sport} -> {p[TCP].dport}")
    if p.haslayer(Raw):
        print(f"Raw data: {bytes(p[Raw])[:50]}")