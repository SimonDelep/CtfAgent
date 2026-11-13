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

# Extraire les octets 3-4 (compteur) comme bytes
counter_bytes = []
for i, pos in enumerate(se_positions):
    counter_bytes.append(data[pos+4:pos+6])

all_counters = b''.join(counter_bytes)
print(f"Total de compteurs: {len(all_counters)} octets")
print(f"Premiers 100 octets: {all_counters[:100]!r}")

# Peut-être que c'est du texte?
print(f"\nInterprété comme ASCII: {all_counters[:100]}")