from scapy.all import *
from scapy.layers.tls.all import *

# Lire le pcap
packets = rdpcap("capture.pcapng")
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premières couches
for i, pkt in enumerate(packets[:5]):
    print(f"Paquet {i}: {pkt.summary()}")