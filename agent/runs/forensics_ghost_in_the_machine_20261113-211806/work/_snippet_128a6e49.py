import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver toutes les positions de deadbeef
dead_beef = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(dead_beef, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

print(f"Nombre de positions: {len(positions)}")
print(f"Premières positions: {positions[:10]}")

# La différence entre positions consécutives devrait nous donner la taille des paquets
diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
print(f"Diffs (tailles entre marqueurs): {set(diffs)}")

# Si chaque paquet a 2 marqueurs, la distance entre marqueurs consécutifs d'un même paquet
# et entre paquets devrait être cohérente