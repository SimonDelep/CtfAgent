import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

dead_beef = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(dead_beef, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Extraire les données entre chaque paire de marqueurs consécutifs (paquets)
# positions[0] et positions[1] sont les deux marqueurs du premier paquet
# positions[2] et positions[3] sont les deux marqueurs du deuxième paquet, etc.

packets_data = []
for i in range(0, len(positions), 2):
    start = positions[i] + 4  # après le premier marqueur
    end = positions[i+1]      # avant le deuxième marqueur
    packet_bytes = data[start:end]
    packets_data.append(packet_bytes)

print(f"Nombre de paquets: {len(packets_data)}")
print(f"Taille de chaque paquet: {[len(p) for p in packets_data[:5]]}")

# Afficher les premières données de paquets
for i, p in enumerate(packets_data[:5]):
    print(f"Paquet {i}: {p.hex()} ({len(p)} octets)")