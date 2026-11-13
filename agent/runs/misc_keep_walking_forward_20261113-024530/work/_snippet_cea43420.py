import sys
sys.path.insert(0, './scapy_lib')
from scapy.all import *

# Lire le PCAP
packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, p in enumerate(packets[:15]):
    print(f"Paquet {i}: {p.summary()}")