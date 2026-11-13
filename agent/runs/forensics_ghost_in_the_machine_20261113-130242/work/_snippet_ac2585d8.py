import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Le fichier commence par le magic number
# Ensuite, il semble y avoir des paquets avec des marqueurs "dead beef"

# Cherchons tous les marqueurs "dead beef"
marker = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

print(f"Nombre de marqueurs dead beef: {len(positions)}")
print(f"Positions des premiers marqueurs: {positions[:20]}")

# Chaque paquet semble avoir 2 marqueurs dead beef
# Regardons la structure entre les marqueurs
print("\nAnalyse de la structure:")
for i in range(0, min(len(positions), 10), 2):
    start = positions[i]
    end = positions[i+1] if i+1 < len(positions) else start + 50
    chunk = data[start:start+50]
    print(f"Paquet {i//2}: offset={start}, hex={chunk.hex()}")