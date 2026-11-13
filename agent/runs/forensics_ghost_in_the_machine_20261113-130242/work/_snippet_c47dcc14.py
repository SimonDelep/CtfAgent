import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Le header PCAP fait 24 octets
# Ensuite, chaque paquet a un header de 16 octets (timestamp + lengths)
# Puis les données du paquet

# Regardons la structure autour du premier paquet
offset = 24
print(f"Header PCAP: {data[0:24].hex()}")

# Header du premier paquet (16 octets)
print(f"Header paquet 1: {data[24:40].hex()}")

# Après le header du paquet, on devrait avoir les données
print(f"Données à partir de 40: {data[40:100].hex()}")

# Chercher le pattern deadbeef
idx = data.find(b'\xde\xad\xbe\xef', 40)
print(f"Premier deadbeef à: {idx}")
print(f"Contexte: {data[idx-5:idx+20].hex()}")
