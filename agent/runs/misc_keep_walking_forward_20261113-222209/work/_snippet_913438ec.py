from scapy.all import *
import sys
sys.path.insert(0, '/tmp/py7zr_pkg')

# Charger le pcap
packets = rdpcap('capture.pcapng')

# Afficher les premiers paquets avec leurs infos
for i, pkt in enumerate(packets[:10]):
    print(f"Packet {i}: {pkt.summary()}")
    if TCP in pkt:
        print(f"  TCP: {pkt[TCP].sport} -> {pkt[TCP].dport}")
        if Raw in pkt:
            print(f"  Raw: {bytes(pkt[Raw])[:50]}")