import struct

# Lire le fichier WAL
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)} octets")
print(f"Magic header: {data[:8].hex()}")

# Le header WAL est de 32 octets
# Ensuite viennent les frames (pages)
# Chaque frame a un header de 24 octets + page_size octets de données

# Page size est stocké aux octets 8-11 (big-endian)
page_size = struct.unpack('>I', data[8:12])[0]
print(f"Page size: {page_size}")

# Nombre de frames
# Le header WAL est de 32 octets, chaque frame est 24 + page_size
# Mais il y a aussi un checksum à la fin

# Cherchons les occurrences de "CSAW" dans le fichier
idx = 0
count = 0
while True:
    idx = data.find(b'CSAW', idx)
    if idx == -1:
        break
    print(f"CSAW trouvé à l'offset {idx}: {data[idx:idx+50].hex()}")
    idx += 1
    count += 1
    if count > 10:
        break
