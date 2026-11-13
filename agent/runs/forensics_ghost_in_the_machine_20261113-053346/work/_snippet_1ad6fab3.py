from scapy.all import rdpcap, UDP
import statistics

# Charger le pcap
packets = rdpcap('capture.pcap')

# Extraire les paquets UDP
udp_packets = [p for p in packets if UDP in p]
print(f"Total paquets UDP: {len(udp_packets)}")

# Analyser les ports sources
src_ports = [p[UDP].sport for p in udp_packets]
from collections import Counter
port_counts = Counter(src_ports)

# Ports fréquents (plusieurs occurrences)
frequent_ports = [p for p, c in port_counts.items() if c > 1]
# Singletons (une seule occurrence)
singleton_ports = [p for p, c in port_counts.items() if c == 1]

print(f"\nPorts fréquents ({len(frequent_ports)}): {sorted(frequent_ports)}")
print(f"Singletons ({len(singleton_ports)}): {sorted(singleton_ports)}")

# Pour chaque singleton, extraire plus d'infos
singleton_packets = []
for i, p in enumerate(udp_packets):
    if p[UDP].sport in singleton_ports:
        singleton_packets.append({
            'index': i,
            'sport': p[UDP].sport,
            'dport': p[UDP].dport,
            'payload': bytes(p[UDP].payload),
            'time': float(p.time)
        })

# Trier par timestamp
singleton_packets.sort(key=lambda x: x['time'])

print("\n=== Détails des 20 premiers singletons (par timestamp) ===")
for sp in singleton_packets[:20]:
    print(f"Idx: {sp['index']}, sport: {sp['sport']}, dport: {sp['dport']}, payload: {sp['payload'][:20]}")

# Vérifier les ports de destination des singletons
singleton_dports = [sp['dport'] for sp in singleton_packets]
print(f"\nPorts de destination des singletons: {set(singleton_dports)}")

# Vérifier si tous les singletons ont le même port de destination
print(f"Tous les singletons ont dport=9000? {len(set(singleton_dports)) == 1 and singleton_dports[0] == 9000}")