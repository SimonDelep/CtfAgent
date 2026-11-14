from scapy.all import rdpcap, UDP

# Charger le pcap
packets = rdpcap('capture.pcap')

print(f"Nombre total de paquets: {len(packets)}")

# Extraire les paquets UDP
udp_packets = [p for p in packets if UDP in p]
print(f"Paquets UDP: {len(udp_packets)}")

# Analyser les ports sources
src_ports = [p[UDP].sport for p in udp_packets]
print(f"Ports sources uniques: {len(set(src_ports))}")

# Compter les occurrences de chaque port
from collections import Counter
port_counts = Counter(src_ports)

# Séparer singletons et fréquents
singletons = [(port, count) for port, count in port_counts.items() if count == 1]
frequent = [(port, count) for port, count in port_counts.items() if count > 1]

print(f"\nSingletons ({len(singletons)}):")
for port, count in sorted(singletons)[:10]:
    print(f"  Port {port}: {count} fois")

print(f"\nPorts fréquents ({len(frequent)}):")
for port, count in sorted(frequent):
    print(f"  Port {port}: {count} fois")