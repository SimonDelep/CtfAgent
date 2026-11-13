from scapy.all import rdpcap, UDP

packets = rdpcap("capture.pcap")

# Séparer les paquets UDP
udp_packets = [p for p in packets if UDP in p]
print(f"Total paquets UDP: {len(udp_packets)}")

# Extraire les ports sources et leurs fréquences
from collections import Counter
src_ports = [p[UDP].sport for p in udp_packets]
port_counts = Counter(src_ports)

# Identifier les singletons (ports qui n'apparaissent qu'une fois)
singletons = [port for port, count in port_counts.items() if count == 1]
frequent = [port for port, count in port_counts.items() if count > 1]

print(f"Ports singletons: {len(singletons)}")
print(f"Ports fréquents: {len(frequent)}")

# Afficher les ports singletons triés par ordre d'apparition
singleton_order = []
for p in udp_packets:
    if p[UDP].sport in singletons:
        singleton_order.append(p[UDP].sport)

print(f"\nPorts singletons dans l'ordre d'apparition:")
print(singleton_order[:20], "...")
print(f"Total: {len(singleton_order)}")

# Afficher les ports fréquents et leurs counts
print(f"\nPorts fréquents (top 10):")
for port, count in port_counts.most_common(10):
    print(f"  Port {port}: {count} fois")