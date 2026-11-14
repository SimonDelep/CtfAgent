# Examiner les 2 octets entre les deux deadbeef
with open('capture.pcap', 'rb') as f:
    data = f.read()

deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    pos = data.find(deadbeef, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

# Pour chaque paquet, regarder les 2 octets entre les deux deadbeef
# Structure: deadbeef (4) + 2b_méta + deadbeef (4) + ...
# Donc les 2 octets de méta sont à position + 4

meta2_bytes_list = []
for i in range(0, len(positions), 2):
    start = positions[i]
    meta2_pos = start + 4
    if meta2_pos + 2 <= len(data):
        meta2 = data[meta2_pos:meta2_pos+2]
        meta2_bytes_list.append(meta2)

print(f"Premières métadonnées (2 octets): {meta2_bytes_list[:20]}")

# Convertir en entiers
meta2_ints = [int.from_bytes(m, 'big') for m in meta2_bytes_list]
print(f"\nPremières valeurs: {meta2_ints[:20]}")

from collections import Counter
meta2_counts = Counter(meta2_ints)
print(f"\nValeurs uniques: {len(meta2_counts)}")
print("Top 10 valeurs:")
for val, count in meta2_counts.most_common(10):
    print(f"  {val}: {count} occurrences")