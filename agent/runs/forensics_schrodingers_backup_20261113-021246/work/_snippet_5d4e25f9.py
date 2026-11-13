import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

# Cherchons toutes les occurrences de "CSAW" et analysons le contexte
idx = 0
occurrences = []
while True:
    idx = data.find(b'CSAW', idx)
    if idx == -1:
        break
    # Regardons 100 octets autour de chaque occurrence
    start = max(0, idx - 10)
    end = min(len(data), idx + 100)
    occurrences.append((idx, data[start:end]))
    idx += 1

print(f"Nombre d'occurrences de CSAW: {len(occurrences)}")

# Analysons la première occurrence
for i, (offset, chunk) in enumerate(occurrences[:5]):
    print(f"\n=== Occurrence {i+1} à l'offset {offset} ===")
    print(f"Hex: {chunk.hex()}")
    # Essayons de décoder ce qui suit CSAW
    after_csaw = chunk[4:]  # Après "CSAW"
    print(f"Après CSAW: {after_csaw[:50].hex()}")
    
    # Cherchons des motifs intéressants
    # 0d00000001 semble être un motif récurrent
    if b'\x0d\x00\x00\x00\x01' in chunk:
        pos = chunk.find(b'\x0d\x00\x00\x00\x01')
        print(f"Motif 0d00000001 trouvé à position {pos} dans le chunk")
        # Après ce motif, il y a souvent 03db00 ou similaire
        if pos + 5 < len(chunk):
            print(f"Données après motif: {chunk[pos:pos+20].hex()}")
