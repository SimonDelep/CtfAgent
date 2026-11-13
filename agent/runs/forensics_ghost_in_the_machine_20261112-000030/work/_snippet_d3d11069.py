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

# Extraire les octets 1-2 (données) comme bytes
data_bytes = []
for i, pos in enumerate(se_positions):
    data_bytes.append(data[pos+2:pos+4])

# Essayer de voir si les bytes forment du texte
all_data = b''.join(data_bytes)
print(f"Total de données: {len(all_data)} octets")
print(f"Premiers 100 octets: {all_data[:100]!r}")

# Peut-être que c'est du texte XORé?
# Ou peut-être que c'est une image?
# Essayons de voir si c'est du texte lisible après XOR avec une clé simple

# Regardons la distribution des bytes
from collections import Counter
byte_counts = Counter(all_data)
print("\nDistribution des bytes (top 20):")
for byte, count in byte_counts.most_common(20):
    print(f"  0x{byte:02x} ({chr(byte) if 32 <= byte < 127 else '.'}): {count}")