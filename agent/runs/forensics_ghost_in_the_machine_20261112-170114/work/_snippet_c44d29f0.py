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

# Tous les ports avec leurs comptes
all_ports = sorted(port_counts.items())
print("All ports with counts:")
for port, count in all_ports:
    print(f"  {port}: {count}")

# Peut-être que le message est dans les ports uniques, mais il faut les trier par un critère différent
# L'indice dit "which columns to trust" - peut-être que certains ports uniques sont du bruit

# Regardons les ports qui apparaissent 2-3 fois
multi_ports = [(p, c) for p, c in port_counts.items() if c > 1 and c < 64]
print(f"\nPorts with 2-3 occurrences: {multi_ports}")

# Peut-être que les ports uniques sont XORés avec les ports fréquents de manière cyclique
# Mais d'abord, regardons si les ports uniques, lorsqu'ils sont XORés avec un offset constant, donnent du texte

# Les ports uniques vont de 50004 à 50996
# Si on soustrait 50000, on obtient des valeurs de 4 à 996
# Pour obtenir des caractères ASCII imprimables (32-126), il faut soustraire environ 50000-48 = 49952 à 50000+126-32 = 50094

# Essayons de trouver un offset qui donne le plus de caractères imprimables
best_offset = 0
best_count = 0
for offset in range(49900, 50100):
    count = 0
    for p in unique_ports_sorted:
        val = p - offset
        if 32 <= val < 127:
            count += 1
    if count > best_count:
        best_count = count
        best_offset = offset

print(f"\nBest offset: {best_offset} with {best_count} printable chars")

# Mais peut-être que le message est XORé avec une clé
# Les ports fréquents sont: 40052, 40100, 40104, 40111, 40115, 40119
# Peut-être que la clé est dérivée de ces ports

key_ports = [40052, 40100, 40104, 40111, 40115, 40119]

# Extraire les ports uniques dans l'ordre d'apparition
unique_in_order = []
seen = set()
for p in packets:
    if port_counts[p] == 1 and p not in seen:
        unique_in_order.append(p)
        seen.add(p)

# Peut-être que la clé est basée sur les positions des ports uniques
# Ou peut-être que chaque port unique est XORé avec un port clé correspondant

# Essayons de XORer chaque port unique avec chaque port clé et voir si on obtient du texte
for key_port in key_ports:
    chars = [chr((p ^ key_port) & 0xFF) if 32 <= (p ^ key_port) & 0xFF < 127 else '?' for p in unique_in_order]
    result = ''.join(chars)
    printable = sum(1 for c in result if c != '?')
    print(f"\nXOR with key_port {key_port}: {printable} printable chars")
    print(f"  First 50: {result[:50]}")

# Peut-être que la clé est la différence entre les ports uniques et quelque chose
# Ou peut-être que la clé est basée sur les timestamps