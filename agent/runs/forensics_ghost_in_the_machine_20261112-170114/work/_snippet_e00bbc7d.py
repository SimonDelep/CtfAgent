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
            packets.append(src_port)

port_counts = Counter(packets)

# Ports uniques
unique_ports = [p for p, c in port_counts.items() if c == 1]
unique_in_order = []
seen = set()
for p in packets:
    if port_counts[p] == 1 and p not in seen:
        unique_in_order.append(p)
        seen.add(p)

# Ports fréquents (la clé potentielle)
key_ports = [40052, 40100, 40104, 40111, 40115, 40119]

print("Trying XOR with each key port:")
for key_port in key_ports:
    chars = [chr((p ^ key_port) & 0xFF) if 32 <= (p ^ key_port) & 0xFF < 127 else '?' for p in unique_in_order]
    result = ''.join(chars)
    printable = sum(1 for c in result if c != '?')
    print(f"\nXOR with {key_port}: {printable}/112 printable")
    print(f"  First 60: {result[:60]}")

# Peut-être que la clé est cyclique
print("\n\nTrying cyclic XOR with key_ports:")
key_cycle = key_ports * (len(unique_in_order) // len(key_ports) + 1)
xored = []
for i, p in enumerate(unique_in_order):
    xored.append(p ^ key_cycle[i % len(key_ports)])

chars = [chr(b & 0xFF) if 32 <= b & 0xFF < 127 else '?' for b in xored]
result = ''.join(chars)
printable = sum(1 for c in result if c != '?')
print(f"Cyclic XOR: {printable}/112 printable")
print(f"Result: {result}")

# Peut-être que la clé est basée sur les ports fréquents d'une manière différente
# Les ports fréquents sont 40052, 40100, 40104, 40111, 40115, 40119
# Peut-être que la clé est la différence entre ces ports et 50000?

key_diffs = [kp - 50000 for kp in key_ports]
print(f"\nKey diffs from 50000: {key_diffs}")

# Ou peut-être que la clé est basée sur les positions
# Regardons si les ports uniques XORés avec leur position donnent quelque chose
print("\n\nTrying XOR with position:")
chars = [chr((p ^ i) & 0xFF) if 32 <= (p ^ i) & 0xFF < 127 else '?' for i, p in enumerate(unique_in_order)]
result = ''.join(chars)
printable = sum(1 for c in result if c != '?')
print(f"XOR with position: {printable}/112 printable")
print(f"Result: {result[:60]}")