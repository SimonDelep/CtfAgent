from scapy.all import *
import binascii

# Charger le pcap
packets = rdpcap('capture.pcapng')

print(f"Total paquets: {len(packets)}")

# Filtrer les paquets TCP
tcp_packets = [p for p in packets if TCP in p]
print(f"Paquets TCP: {len(tcp_packets)}")

# Afficher les ports
ports = set()
for p in tcp_packets:
    ports.add((p[TCP].sport, p[TCP].dport))
print(f"Ports utilisés: {ports}")

# Extraire les paquets sur les ports 443 et 4433
target_packets = [p for p in tcp_packets if p[TCP].dport in [443, 4433] or p[TCP].sport in [443, 4433]]
print(f"Paquets sur 443/4433: {len(target_packets)}")

# Afficher les 10 premiers paquets avec leurs ports
for i, p in enumerate(target_packets[:10]):
    payload_len = len(p[TCP].payload) if p[TCP].payload else 0
    print(f"Paquet {i}: sport={p[TCP].sport}, dport={p[TCP].dport}, payload_len={payload_len}")