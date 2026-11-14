# Re-extraction des données du pcap custom
import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Magic number custom
magic = data[:4]
print(f"Magic: {magic.hex()}")

# En-tête global de 40 octets
header = data[4:40]
print(f"Header length: {len(header)}")

# Trouver tous les marqueurs deadbeef
deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    pos = data.find(deadbeef, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

print(f"Nombre de marqueurs deadbeef: {len(positions)}")
print(f"Positions des 10 premiers: {positions[:10]}")

# Structure: deadbeef + 2 octets + deadbeef + 4 octets méta + IP + UDP + payload
# Chaque paquet a 2 marqueurs deadbeef
num_packets = len(positions) // 2
print(f"Nombre de paquets: {num_packets}")