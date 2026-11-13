from scapy.all import *
import binascii

# Lire le pcapng
packets = rdpcap("capture.pcapng")

print(f"Nombre total de paquets: {len(packets)}")

# Analyser les protocoles
from collections import Counter
protocols = Counter()
for p in packets:
    if p.haslayer(IP):
        protocols[p[IP].proto] += 1

print(f"Protocoles IP: {protocols}")

# Regarder les ports
ports = Counter()
for p in packets:
    if p.haslayer(TCP):
        ports[(p[TCP].sport, p[TCP].dport)] += 1

print(f"Ports TCP (sport, dport): {dict(ports)}")

# Afficher quelques paquets
for i, p in enumerate(packets[:10]):
    print(f"\n--- Paquet {i} ---")
    p.show()