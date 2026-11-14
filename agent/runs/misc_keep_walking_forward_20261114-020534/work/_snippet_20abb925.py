#!/usr/bin/env python3
from scapy.all import *

# Charger le pcap
packets = rdpcap("capture.pcapng")

print(f"Nombre total de paquets: {len(packets)}")

# Trouver les paquets TLS (port 443 ou 4433)
tls_packets = []
for i, pkt in enumerate(packets):
    if TCP in pkt and (pkt[TCP].dport == 443 or pkt[TCP].sport == 443 or 
                       pkt[TCP].dport == 4433 or pkt[TCP].sport == 4433):
        if Raw in pkt:
            data = bytes(pkt[Raw].load)
            # Vérifier si c'est un en-tête TLS
            if len(data) >= 5:
                content_type = data[0]
                version = data[1:3]
                length = struct.unpack("!H", data[3:5])[0]
                print(f"Paquet {i}: port={pkt[TCP].dport}/{pkt[TCP].sport}, content_type=0x{content_type:02x}, version=0x{version.hex()}, length={length}")
                if content_type == 0x17:  # Application Data
                    print(f"  -> APPLICATION DATA! (taille données: {len(data)})")
                    tls_packets.append((i, pkt, data))

print(f"\nTotal paquets TLS avec Raw: {len(tls_packets)}")
