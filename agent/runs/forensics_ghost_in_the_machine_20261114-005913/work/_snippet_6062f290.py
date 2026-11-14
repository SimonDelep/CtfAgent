with open('capture.pcap', 'rb') as f:
    data = f.read()

# Premier paquet commence à position 40
# deadbeef à 40-43
# 2 octets à 44-45
# deadbeef à 46-49
# Ensuite...

print("Analyse du premier paquet:")
print(f"Positions 40-60: {data[40:61].hex()}")
print(f"Positions 40-60 (repr): {data[40:61]}")

# deadbeef à 40-43
# 2 octets à 44-45: c'est le timestamp?
# deadbeef à 46-49
# Après 49:

print(f"Positions 50-70: {data[50:71].hex()}")

# Regardons où commence l'IP (0x45)
for i in range(50, 80):
    if data[i] == 0x45:
        print(f"0x45 trouvé à position {i}")
        print(f"Positions {i}-{i+20}: {data[i:i+20].hex()}")
        break

# L'IP header:
# Octet 0: 0x45 (version 4, IHL 5 = 20 octets)
# Octets 12-15: source IP
# Octets 16-19: dest IP
# Après IP header (20 octets): UDP header
# UDP header: port source (2 octets), port dest (2 octets), length (2 octets), checksum (2 octets)
# Puis payload

# Si IP commence à position i, alors:
# src_port = data[i+20: i+22]
# dst_port = data[i+22: i+24]

# Trouvons tous les 0x45 qui sont des débuts d'IP
ip_starts = []
for i in range(40, len(data)-20):
    if data[i] == 0x45 and (data[i+1] & 0xF0) == 0x40:  # Version 4
        # Vérifier que c'est bien un header IP valide
        ihl = data[i] & 0x0F
        if ihl == 5:  # 20 octets
            ip_starts.append(i)

print(f"\nNombre de débuts d'IP trouvés: {len(ip_starts)}")
print(f"Premiers 10 positions IP: {ip_starts[:10]}")

# Extraire les ports sources
ports = []
for ip_start in ip_starts:
    # IP header = 20 octets (IHL=5)
    udp_start = ip_start + 20
    if udp_start + 2 <= len(data):
        src_port = int.from_bytes(data[udp_start:udp_start+2], 'big')
        dst_port = int.from_bytes(data[udp_start+2:udp_start+4], 'big')
        ports.append((src_port, dst_port))

print(f"\nNombre de ports extraits: {len(ports)}")
print(f"Premiers 10 ports (src, dst): {ports[:10]}")

# Compter les singletons
from collections import Counter
src_ports = [p[0] for p in ports]
port_counts = Counter(src_ports)
singletons = [p for p, c in port_counts.items() if c == 1]
print(f"\nNombre de singletons: {len(singletons)}")
print(f"Singletons (triés): {sorted(singletons)[:20]}")

# Ports fréquents
frequent = [(p, c) for p, c in port_counts.items() if c > 1]
frequent_sorted = sorted(frequent, key=lambda x: -x[1])
print(f"\nPorts fréquents (top 10): {frequent_sorted[:10]}")
