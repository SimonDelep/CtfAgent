from scapy.all import *
import binascii

# Lire le PCAP
packets = rdpcap('capture.pcapng')

# Afficher les infos de base
print(f"Nombre de paquets: {len(packets)}")

# Trouver les paquets TCP sur le port 443
tcp_443 = [p for p in packets if TCP in p and (p[TCP].dport == 443 or p[TCP].sport == 443)]
print(f"Paquets TCP port 443: {len(tcp_443)}")

# Afficher les premiers paquets
for i, p in enumerate(packets[:10]):
    print(f"Paquet {i}: {p.summary()}")