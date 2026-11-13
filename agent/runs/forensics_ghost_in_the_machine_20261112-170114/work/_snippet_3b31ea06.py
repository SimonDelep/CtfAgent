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

# Ports uniques triés par valeur
unique_ports_sorted = sorted([p for p, c in port_counts.items() if c == 1])
print(f"Unique ports sorted: {unique_ports_sorted}")
print(f"Count: {len(unique_ports_sorted)}")

# Les ports uniques vont de 50004 à 50996
# Peut-être que le message est encodé en soustrayant 50000 et en prenant le résultat
# Mais il y a 112 ports uniques, ce qui est beaucoup pour un flag

# Peut-être que certains ports uniques sont du bruit aussi
# Regardons la distribution des ports uniques
print(f"\nMin unique port: {min(unique_ports_sorted)}")
print(f"Max unique port: {max(unique_ports_sorted)}")

# Peut-être que le message est dans les ports uniques, mais il faut les trier par ordre d'apparition
# et ensuite appliquer une transformation

# Extraire les ports uniques dans l'ordre d'apparition
unique_in_order = []
seen = set()
for p in packets:
    if port_counts[p] == 1 and p not in seen:
        unique_in_order.append(p)
        seen.add(p)

print(f"\nUnique ports in order of appearance: {unique_in_order}")

# Peut-être que le message est XORé avec une clé dérivée des ports fréquents
# Les ports fréquents sont: 40052, 40100, 40104, 40111, 40115, 40119
# Peut-être que la clé est la différence entre ces ports et quelque chose

key_ports = [40052, 40100, 40104, 40111, 40115, 40119]
print(f"\nKey ports: {key_ports}")

# Différences entre ports fréquents
diffs = [key_ports[i+1] - key_ports[i] for i in range(len(key_ports)-1)]
print(f"Differences between key ports: {diffs}")

# Peut-être que la clé est basée sur ces différences
# Ou peut-être que la clé est simplement les 6 ports fréquents utilisés de manière cyclique

# Essayons de soustraire 50000 des ports uniques et voir si on obtient du texte
offset = 50000
chars = [chr(p - offset) if 32 <= p - offset < 127 else '?' for p in unique_in_order]
print(f"\nWith offset 50000 (order): {''.join(chars)}")

# Essayons avec les ports triés par valeur
chars_sorted = [chr(p - offset) if 32 <= p - offset < 127 else '?' for p in unique_ports_sorted]
print(f"With offset 50000 (sorted): {''.join(chars_sorted)}")

# Peut-être que l'offset n'est pas 50000
# Regardons les valeurs possibles
for offset in range(49900, 50100, 10):
    chars = [chr(p - offset) if 32 <= p - offset < 127 else '?' for p in unique_in_order[:10]]
    result = ''.join(chars)
    if '?' not in result:
        print(f"Offset {offset}: {result}")