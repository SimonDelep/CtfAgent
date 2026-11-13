with open('capture.pcap', 'rb') as f:
    data = f.read()

# Extraire les 4 octets après chaque "Se"
se_positions = []
pos = 0
while True:
    pos = data.find(b'Se', pos)
    if pos == -1:
        break
    se_positions.append(pos)
    pos += 1

# Extraire les octets 3-4 (compteur) et les octets 1-2 (données)
counter_values = []
data_values = []

for i, pos in enumerate(se_positions):
    counter = int.from_bytes(data[pos+4:pos+6], 'little')
    data_val = int.from_bytes(data[pos+2:pos+4], 'little')
    counter_values.append(counter)
    data_values.append(data_val)

# Compter les occurrences de chaque valeur de compteur
from collections import Counter
counter_counts = Counter(counter_values)
print("Distribution des valeurs de compteur:")
for k, v in sorted(counter_counts.items()):
    print(f"  {k}: {v} occurrences")

print(f"\nTotal: {sum(counter_counts.values())} paquets")
print(f"Valeurs uniques de compteur: {len(counter_counts)}")