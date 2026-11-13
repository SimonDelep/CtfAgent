import sys
sys.path.insert(0, '/tmp/scapy_pkg')
from scapy.all import *

packets = rdpcap('capture.pcapng')

# Filtrer les paquets TCP
tcp_packets = [p for p in packets if p.haslayer(TCP)]
print(f"Nombre de paquets TCP: {len(tcp_packets)}")

# Afficher les ports TCP utilisés
ports = set()
for p in tcp_packets:
    if p.haslayer(TCP):
        ports.add((p[TCP].sport, p[TCP].dport))
print(f"Ports TCP observés: {sorted(ports)[:20]}")

# Afficher les paquets TCP avec Raw
for i, pkt in enumerate(tcp_packets[:10]):
    print(f"\nPaquet TCP {i}:")
    print(f"  {pkt[IP].src}:{pkt[TCP].sport} -> {pkt[IP].dst}:{pkt[TCP].dport}")
    if pkt.haslayer(Raw):
        raw_data = pkt[Raw].load
        print(f"  Raw ({len(raw_data)} bytes): {raw_data[:100]}")