from scapy.all import *
import binascii

# Lire le pcapng
packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, pkt in enumerate(packets[:10]):
    print(f"Paquet {i}: {pkt.summary()}")