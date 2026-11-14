with open('capture.pcap', 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)} octets")
print(f"Premiers 100 octets: {data[:100].hex()}")
print()

# Chercher deadbeef dans tout le fichier
deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    idx = data.find(deadbeef, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

print(f"Nombre de marqueurs deadbeef: {len(positions)}")
print(f"Positions: {positions[:20]}")

# Vérifier aussi l'ordre inverse (little-endian)
deadbeef_le = b'\xef\xbe\xad\xde'
positions_le = []
pos = 0
while True:
    idx = data.find(deadbeef_le, pos)
    if idx == -1:
        break
    positions_le.append(idx)
    pos = idx + 1

print(f"Nombre de marqueurs efbeadde: {len(positions_le)}")
if positions_le:
    print(f"Positions efbeadde: {positions_le[:20]}")
