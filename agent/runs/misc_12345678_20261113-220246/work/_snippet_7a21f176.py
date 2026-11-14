import struct

with open('audio.wav', 'rb') as f:
    data = f.read()

# Structure RIFF: RIFF + taille + WAVE + chunks
# RIFF header: 12 octets (RIFF + 4 bytes taille + WAVE)
# Ensuite les chunks

pos = 12  # Après "RIFF" + taille + "WAVE"
chunks = []

while pos < len(data) - 8:
    chunk_id = data[pos:pos+4].decode('ascii', errors='ignore')
    if len(chunk_id) != 4:
        pos += 1
        continue
        
    if pos + 8 > len(data):
        break
        
    chunk_size = struct.unpack('<I', data[pos+4:pos+8])[0]
    
    # S'assurer qu'on a assez de données
    if pos + 8 + chunk_size > len(data):
        # Chunk incomplet, essayer de continuer
        chunks.append((chunk_id, pos, chunk_size, data[pos:pos+8+min(chunk_size, 100)]))
        break
    
    chunks.append((chunk_id, pos, chunk_size))
    
    # Avancer au prochain chunk (aligné sur 2 octets)
    pos += 8 + chunk_size
    if chunk_size % 2 == 1:
        pos += 1  # Padding

print(f"Nombre de chunks: {len(chunks)}")
for i, chunk in enumerate(chunks[:20]):
    chunk_id, start, size = chunk[0], chunk[1], chunk[2]
    print(f"  {i}: {chunk_id} offset={start} size={size}")
    if chunk_id in ['LIST', 'INFO', 'ID3 ', 'ID3v']:
        chunk_data = data[start+8:start+8+size]
        print(f"      Contenu: {chunk_data[:300]}")