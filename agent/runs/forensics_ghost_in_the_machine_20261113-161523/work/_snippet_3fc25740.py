# D'abord, obtenons l'ordre d'apparition des ports fréquents
# et voyons si on peut extraire la clé

# Re-lisons le pcap pour obtenir l'ordre d'apparition des ports
import struct

with open('capture.pcap', 'rb') as f:
    magic = f.read(4)
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 14 + 20 + 8:
            # Ethernet + IP + UDP
            ether_type = struct.unpack('>H', pkt_data[12:14])[0]
            if ether_type == 0x0800:
                protocol = pkt_data[23]  # IP header, byte 9 (0-indexed from IP start)
                if protocol == 17:  # UDP
                    src_port = struct.unpack('>H', pkt_data[34:36])[0]
                    dst_port = struct.unpack('>H', pkt_data[36:38])[0]
                    packets.append((ts_sec, ts_usec, src_port, dst_port))

# Compter les occurrences
from collections import Counter, OrderedDict
src_ports = [p[2] for p in packets]
port_counts = Counter(src_ports)

# Ports fréquents (plus d'une occurrence)
frequent = {port: count for port, count in port_counts.items() if count > 1}
print("Ports fréquents avec leurs comptes:")
for port, count in sorted(frequent.items(), key=lambda x: -x[1]):
    print(f"  {port}: {count} occurrences")

# Singletons
singletons = [port for port, count in port_counts.items() if count == 1]
print(f"\nNombre de singletons: {len(singletons)}")

# Ordre d'apparition des singletons
singleton_order = []
seen = set()
for ts, ts_usec, port, dst in packets:
    if port_counts[port] == 1 and port not in seen:
        singleton_order.append(port)
        seen.add(port)

print(f"\nPremiers 20 singletons dans l'ordre:")
print(singleton_order[:20])

# Maintenant, regardons les ports fréquents dans l'ordre d'apparition
frequent_order = []
seen_frequent = set()
for ts, ts_usec, port, dst in packets:
    if port_counts[port] > 1 and port not in seen_frequent:
        frequent_order.append(port)
        seen_frequent.add(port)

print(f"\nPorts fréquents dans l'ordre d'apparition:")
print(frequent_order)

# Peut-être que la clé est dérivée de ces ports
# Essayons de convertir les ports fréquents en ASCII
print("\nPorts fréquents modulo 256:")
for p in frequent_order:
    print(f"{p} -> {p % 256} -> {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")