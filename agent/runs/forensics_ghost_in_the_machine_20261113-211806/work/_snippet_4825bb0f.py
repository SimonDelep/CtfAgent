from scapy.all import rdpcap, UDP
from collections import Counter

packets = rdpcap('capture.pcap')
udp_packets = [p for p in packets if UDP in p]

# Extraire ports sources dans l'ordre
src_ports = [(i, p[UDP].sport) for i, p in enumerate(udp_packets)]

# Compter occurrences
port_counts = Counter([sport for _, sport in src_ports])

# Séparer singletons et fréquents
singletons = [(idx, port) for idx, port in src_ports if port_counts[port] == 1]
frequent_ports = [(idx, port) for idx, port in src_ports if port_counts[port] > 1]

print(f"Total paquets UDP: {len(udp_packets)}")
print(f"Singletons: {len(singletons)}")
print(f"Ports fréquents: {len(frequent_ports)}")

# Afficher les ports fréquents uniques
unique_frequent = sorted(set(port for _, port in frequent_ports))
print(f"\nPorts fréquents uniques ({len(unique_frequent)}): {unique_frequent}")

# Afficher les singletons dans l'ordre
singleton_ports = [port for _, port in singletons]
print(f"\nPremiers 20 singletons (ordre chronologique): {singleton_ports[:20]}")
print(f"Derniers 20 singletons: {singleton_ports[-20:]}")