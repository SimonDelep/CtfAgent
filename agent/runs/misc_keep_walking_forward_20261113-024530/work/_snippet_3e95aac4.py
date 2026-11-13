import sys
sys.path.insert(0, './scapy_lib')
from scapy.all import *

# Lire le PCAP
packets = rdpcap('capture.pcapng')

# Extraire les paquets TCP avec données Raw sur le port 443
# Reconstruire le flux dans l'ordre
tcp_stream = []
for p in packets:
    if TCP in p and p.haslayer(Raw):
        if p[TCP].dport == 443 or p[TCP].sport == 443:
            tcp_stream.append(p)

# Trier par numéro de séquence pour reconstruire le flux
# Mais d'abord, voyons si on peut extraire les données TLS brutes
all_data = b''
for p in tcp_stream:
    raw_data = bytes(p[Raw].load)
    all_data += raw_data

print(f"Total de données TLS brutes: {len(all_data)} bytes")
print(f"Premiers 100 bytes: {all_data[:100].hex()}")