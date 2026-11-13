import sys
sys.path.insert(0, './scapy_lib')
from scapy.all import *

# Lire le pcapng
packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, pkt in enumerate(packets[:5]):
    print(f"Paquet {i}: {pkt.summary()}")