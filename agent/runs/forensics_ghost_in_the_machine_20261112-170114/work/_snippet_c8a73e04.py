import struct
from collections import Counter

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 28:
            src_port = struct.unpack('>H', pkt_data[34:36])[0]
            dst_port = struct.unpack('>H', pkt_data[36:38])[0]
            packets.append({'src_port': src_port, 'dst_port': dst_port})

port_counts = Counter(p['src_port'] for p in packets)

# Tous les ports et leurs comptes
print("All ports with counts:")
for port, count in sorted(port_counts.items()):
    print(f"  {port}: {count}")

# Peut-être que le message est dans les ports uniques, mais XORé avec quelque chose
# Les 6 ports fréquents pourraient être une clé cyclique
key_ports = [40052, 40100, 40104, 40111, 40115, 40119]
print(f"\nKey ports: {key_ports}")

# Extraire les ports uniques dans l'ordre d'apparition
unique_in_order = []
seen = set()
for p in packets:
    sp = p['src_port']
    if port_counts[sp] == 1 and sp not in seen:
        unique_in_order.append(sp)
        seen.add(sp)

print(f"\nUnique ports in order: {unique_in_order}")

# Essayer XOR avec les ports clés
# Peut-être que chaque port unique est XORé avec un port clé correspondant
# Ou peut-être que la clé est dérivée des ports clés

# D'abord, regardons si les ports uniques XORés avec quelque chose donnent du texte
# Essayons de trouver un pattern

# Peut-être que les ports uniques sont XORés avec les ports clés de manière cyclique
key_cycle = key_ports * (len(unique_in_order) // len(key_ports) + 1)

# XOR chaque port unique avec le port clé correspondant
xored = []
for i, up in enumerate(unique_in_order):
    kp = key_cycle[i % len(key_ports)]
    xored.append(up ^ kp)

print(f"\nXOR with key cycle: {xored[:20]}")

# Convertir en ASCII
chars = [chr(b) if 32 <= b < 127 else '?' for b in xored]
print(f"As chars: {''.join(chars)[:50]}...")