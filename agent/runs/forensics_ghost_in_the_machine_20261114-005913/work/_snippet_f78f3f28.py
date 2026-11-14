with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver tous les débuts d'IP (0x45 suivi de version 4)
ip_starts = []
for i in range(40, len(data)-40):
    if data[i] == 0x45:
        # Vérifier que c'est un header IP valide
        ihl = data[i] & 0x0F
        version = (data[i] >> 4) & 0x0F
        if version == 4 and ihl == 5:
            # Vérifier que les octets 12-15 sont des IPs valides (10.x.x.x)
            if data[i+12] == 0x0a:  # 10.x.x.x
                ip_starts.append(i)

print(f"Nombre de débuts d'IP trouvés: {len(ip_starts)}")
print(f"Premiers 10 positions IP: {ip_starts[:10]}")

# Extraire les ports sources
ports = []
timestamps = []
for ip_start in ip_starts:
    udp_start = ip_start + 20
    if udp_start + 2 <= len(data):
        src_port = int.from_bytes(data[udp_start:udp_start+2], 'big')
        dst_port = int.from_bytes(data[udp_start+2:udp_start+4], 'big')
        ports.append(src_port)
        
        # Le timestamp est dans les 2 octets avant le deuxième deadbeef
        # Trouver le deadbeef avant cette IP
        # Les deadbeef sont à positions[i] et positions[i+1]
        # L'IP est à positions[i+1] + 4 + 4 = positions[i+1] + 8
        # Donc positions[i+1] = ip_start - 8
        # Et le timestamp est à positions[i+1] - 2 = ip_start - 10
        
        ts_pos = ip_start - 10
        if ts_pos >= 0:
            ts = int.from_bytes(data[ts_pos:ts_pos+2], 'big')
            timestamps.append(ts)

print(f"\nNombre de ports extraits: {len(ports)}")
print(f"Premiers 10 ports: {ports[:10]}")
print(f"Premiers 10 timestamps: {timestamps[:10]}")

# Compter les singletons
from collections import Counter
port_counts = Counter(ports)
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"\nNombre de singletons: {len(singletons)}")
print(f"Singletons (triés par valeur): {sorted(singletons)[:20]}")

# Ports fréquents
frequent = [(p, c) for p, c in port_counts.items() if c > 1]
frequent_sorted = sorted(frequent, key=lambda x: -x[1])
print(f"\nPorts fréquents (top 10): {frequent_sorted[:10]}")

# Vérifier la clé "sh4dow"
top6_ports = [p for p, c in frequent_sorted[:6]]
print(f"\nTop 6 ports: {top6_ports}")
key_bytes = [p % 256 for p in top6_ports]
print(f"Key bytes: {key_bytes}")
print(f"Key string: {bytes(key_bytes).decode('utf-8', errors='replace')}")
