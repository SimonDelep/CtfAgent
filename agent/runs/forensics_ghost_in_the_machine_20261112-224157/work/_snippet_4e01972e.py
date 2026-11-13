with open('capture.pcap', 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes")
print(f"First 100 bytes hex: {data[:100].hex()}")
print(f"First 100 bytes: {data[:100]}")

# Look for "PING" occurrences
ping_count = data.count(b'PING')
print(f"\n'PING' occurrences: {ping_count}")

# Find positions of "PING"
positions = []
pos = 0
while True:
    pos = data.find(b'PING', pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

print(f"\nFirst 20 PING positions: {positions[:20]}")

# Check spacing between PINGs
if len(positions) > 1:
    spacings = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    print(f"\nSpacing between PINGs:")
    print(f"  Min: {min(spacings)}")
    print(f"  Max: {max(spacings)}")
    print(f"  Unique spacings: {len(set(spacings))}")
    print(f"  Most common spacing: {max(set(spacings), key=spacings.count)}")