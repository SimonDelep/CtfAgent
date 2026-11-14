import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Regardons le début du fichier après l'en-tête
# Magic: c4c3b2a1 (4 octets)
# Ensuite, cherchons la structure

# Premier marqueur deadbeef est à position 40
# Donc en-tête global = 40 octets (4 magic + 36 en-tête)

print("En-tête global (positions 4-40):")
print(data[4:40].hex())

# Regardons autour du premier marqueur
print("\nAutour du premier marqueur (position 40):")
print(f"Positions 36-50: {data[36:50].hex()}")

# Structure supposée:
# [deadbeef] [données du paquet] [deadbeef]
# Mais peut-être que les données du paquet sont plus grandes

# Cherchons le deuxième marqueur
dead_beef = bytes.fromhex('deadbeef')
pos1 = data.find(dead_beef, 40)
pos2 = data.find(dead_beef, pos1 + 1)
print(f"\nPremier marqueur à: {pos1}")
print(f"Deuxième marqueur à: {pos2}")
print(f"Données entre marqueurs: {data[pos1+4:pos2].hex()}")
print(f"Longueur: {pos2 - pos1 - 4}")

# Regardons plus de contexte
print(f"\nPositions 40-110: {data[40:110].hex()}")