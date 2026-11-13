from scapy.all import *

# Lire le PCAP
packets = rdpcap("capture.pcap")
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, pkt in enumerate(packets[:10]):
    print(f"\n--- Paquet {i} ---")
    pkt.show()