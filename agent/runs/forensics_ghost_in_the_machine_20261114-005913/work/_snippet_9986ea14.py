# Examiner les métadonnées entre les deadbeef et l'IP
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

# Pour chaque paquet, regarder les 4 octets entre le deuxième deadbeef et l'IP
# Structure: deadbeef (4) + 2b + deadbeef (4) + 4b_méta + IP
# Donc les 4 octets de méta sont à position + 4 + 2 + 4 = position + 10

meta_bytes_list = []
for i in range(0, len(positions), 2):
    start = positions[i]
    meta_pos = start + 10
    if meta_pos + 4 <= len(data):
        meta = data[meta_pos:meta_pos+4]
        meta_bytes_list.append(meta)

print(f"Nombre de métadonnées: {len(meta_bytes_list)}")
print(f"Premières métadonnées: {meta_bytes_list[:10]}")

# Convertir en entiers
meta_ints = [int.from_bytes(m, 'big') for m in meta_bytes_list]
print(f"\nPremières valeurs entières: {meta_ints[:20]}")

# Vérifier si ces valeurs ont un motif
from collections import Counter
meta_counts = Counter(meta_ints)
print(f"\nValeurs uniques de méta: {len(meta_counts)}")
print("Top 10 valeurs méta:")
for val, count in meta_counts.most_common(10):
    print(f"  {val}: {count} occurrences")