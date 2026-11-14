# Re-analyse du fichier capture.pcap
# Structure connue: Magic c4c3b2a1, en-tête 40 octets, paquets délimités par deadbeef

with open('capture.pcap', 'rb') as f:
    data = f.read()

print(f"Taille fichier: {len(data)} octets")
print(f"Magic number: {data[:4].hex()}")

# Trouver toutes les occurrences de deadbeef
deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    pos = data.find(deadbeef, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

print(f"Nombre d'occurrences de deadbeef: {len(positions)}")
print(f"Positions des 10 premiers: {positions[:10]}")

# Vérifier l'espacement entre occurrences
if len(positions) >= 2:
    diffs = [positions[i+1] - positions[i] for i in range(min(10, len(positions)-1))]
    print(f"Diffs entre occurrences: {diffs}")