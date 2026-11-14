import sys
sys.path.insert(0, '/tmp/scapy_lib')
from scapy.all import *
from scapy.layers.tls.all import *
from scapy.layers.tls.session import *
import binascii

# Lire le pcap
packets = rdpcap('capture.pcapng')

# Trouver les paquets TLS
tls_packets = []
for pkt in packets:
    if TLS in pkt:
        tls_packets.append(pkt)

print(f"Paquets TLS trouvés: {len(tls_packets)}")

# Afficher les détails des paquets TLS
for i, pkt in enumerate(tls_packets[:5]):
    print(f"\n--- Paquet TLS {i} ---")
    print(pkt.show())