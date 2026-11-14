# Debug: examiner la structure entre les marqueurs
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

print(f"Total positions: {len(positions)}")
print(f"Positions[0:10]: {positions[:10]}")

# Distance entre positions consécutives
for i in range(min(10, len(positions)-1)):
    dist = positions[i+1] - positions[i]
    print(f"Distance entre positions[{i}] et positions[{i+1}]: {dist}")

# Examiner le contenu autour des positions
print("\nContenu autour de positions[0]:")
start = positions[0]
print(f"Bytes {start}:{start+20}: {data[start:start+20].hex()}")

print(f"\nContenu autour de positions[1]:")
start = positions[1]
print(f"Bytes {start}:{start+20}: {data[start:start+20].hex()}")

# Positions[0] = 40, positions[1] = 46, distance = 6
# Donc entre les deux deadbeef il y a 2 octets (46-40-4=2)
# positions[1] = 46, positions[2] = 102, distance = 56
# Entre positions[1] et positions[2]: 56-4 = 52 octets de données