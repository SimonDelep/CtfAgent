import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024
frame_header_size = 8
frame_size = frame_header_size + page_size

# La différence entre taille réelle et attendue
diff = len(data) - (32 + 39 * frame_size)
print(f"Difference: {diff} octets")

# Peut-être que le header WAL est plus grand ou il y a un padding
# Essayons de trouver toutes les occurrences de 32 octets non-nuls

# Chercher des séquences de 32 octets avec peu de zéros
candidates = []
for i in range(len(data) - 32):
    chunk = data[i:i+32]
    null_count = chunk.count(b'\x00')
    if null_count < 10:  # moins de 10 zéros
        candidates.append((i, chunk, null_count))

print(f"Nombre de candidats potentiels: {len(candidates)}")

# Afficher les premiers candidats
for pos, chunk, nulls in candidates[:20]:
    print(f"Pos {pos}: nulls={nulls}, hex={chunk.hex()}")