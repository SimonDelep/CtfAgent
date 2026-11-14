import struct

pcap_file = 'capture.pcap'

with open(pcap_file, 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)} octets")
print(f"Magic number (4 premiers octets): {data[:4].hex()}")

# Trouver tous les marqueurs deadbeef
marker = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

print(f"Nombre de marqueurs deadbeef trouvés: {len(positions)}")
print(f"Positions des premiers deadbeef: {positions[:10]}")

# Vérifier la structure autour du premier deadbeef après l'en-tête (40 octets)
# L'en-tête global fait 40 octets, puis devrait y avoir deadbeef
print(f"\nDonnées autour de l'offset 40: {data[38:50].hex()}")