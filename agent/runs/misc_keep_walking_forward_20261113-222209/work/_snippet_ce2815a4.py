import sys
sys.path.insert(0, '/tmp/scapy_lib')
from scapy.all import *
from scapy.layers.tls.all import *

# Lire le pcap
packets = rdpcap('capture.pcapng')
print(f"Total paquets: {len(packets)}")

# Afficher les types de paquets
for i, pkt in enumerate(packets[:10]):
    print(f"Paquet {i}: {pkt.summary()}")