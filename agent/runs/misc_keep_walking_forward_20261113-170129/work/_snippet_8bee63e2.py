from scapy.all import *
from scapy.layers.tls.all import *
import binascii

# Lire le pcap
packets = rdpcap('capture.pcapng')

# Afficher les paquets TLS/HTTPS
for i, pkt in enumerate(packets):
    if TCP in pkt:
        print(f"Packet {i}: {pkt[IP].src}:{pkt[TCP].sport} -> {pkt[IP].dst}:{pkt[TCP].dport} [{pkt[TCP].flags}]")
        if Raw in pkt:
            data = bytes(pkt[Raw].load)
            print(f"  Raw data (first 50 bytes): {data[:50]}")