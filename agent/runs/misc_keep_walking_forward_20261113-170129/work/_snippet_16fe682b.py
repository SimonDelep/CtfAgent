import sys
sys.path.insert(0, '/tmp/scapy_pkg')
from scapy.all import *

# Lire le pcapng
packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, pkt in enumerate(packets[:5]):
    print(f"\nPaquet {i}:")
    print(pkt.summary())
    if pkt.haslayer(Raw):
        print(f"  Raw: {pkt[Raw].load[:50]}")