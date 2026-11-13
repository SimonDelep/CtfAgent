import sys
sys.path.insert(0, './scapy_lib')
from scapy.all import *

packets = rdpcap('capture.pcapng')

# Trouver les paquets TCP
tcp_packets = [p for p in packets if TCP in p]
print(f"Nombre de paquets TCP: {len(tcp_packets)}")

# Afficher les ports utilisés
ports = set()
for p in tcp_packets:
    if TCP in p:
        ports.add((p[TCP].sport, p[TCP].dport))
print(f"Ports TCP: {ports}")

# Afficher les premiers paquets TCP
for i, pkt in enumerate(tcp_packets[:10]):
    print(f"Paquet TCP {i}: {pkt.summary()}")