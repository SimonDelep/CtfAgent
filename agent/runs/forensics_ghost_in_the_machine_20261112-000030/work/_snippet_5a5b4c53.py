from scapy.all import rdpcap, ICMP, Raw
import os

# Essayer de lire le pcap
try:
    packets = rdpcap('capture.pcap')
    print(f"Nombre de paquets: {len(packets)}")
    if len(packets) > 0:
        print(f"Premier paquet: {packets[0].summary()}")
        if packets[0].haslayer(Raw):
            print(f"Raw layer: {bytes(packets[0][Raw]).hex()[:100]}")
except Exception as e:
    print(f"Erreur: {e}")