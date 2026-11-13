from scapy.all import *
import binascii

# Lire le PCAP
packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets pour comprendre la structure
for i, pkt in enumerate(packets[:5]):
    print(f"Paquet {i}: {pkt.summary()}")
    if pkt.haslayer('Raw'):
        print(f"  Raw: {bytes(pkt['Raw'])[:50]}")