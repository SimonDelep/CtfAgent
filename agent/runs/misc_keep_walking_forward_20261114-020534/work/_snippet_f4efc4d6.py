from scapy.all import *
import binascii

# Lire le pcap
packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, pkt in enumerate(packets[:20]):
    print(f"\n--- Paquet {i} ---")
    print(pkt.summary())
    if pkt.haslayer('Raw'):
        raw = bytes(pkt['Raw'].load)
        print(f"Raw data (hex): {binascii.hexlify(raw[:50]).decode()}")