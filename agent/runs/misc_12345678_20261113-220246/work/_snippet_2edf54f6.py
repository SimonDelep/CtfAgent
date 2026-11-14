# Analyser la structure du fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher les chunks WAV
import struct

pos = 0
chunks = []

while pos < len(data) - 8:
    chunk_id = data[pos:pos+4].decode('ascii', errors='ignore')
    if chunk_id in ['RIFF', 'WAVE', 'fmt ', 'data', 'LIST', 'INFO', 'ID3 ', 'ID32', 'ID3v']:
        if pos + 8 <= len(data):
            chunk_size = struct.unpack('<I', data[pos+4:pos+8])[0]
            chunks.append((chunk_id, pos, chunk_size))
            pos += 8 + chunk_size
        else:
            pos += 1
    else:
        pos += 1

print("Chunks trouvés:")
for chunk_id, start, size in chunks:
    print(f"  {chunk_id}: offset={start}, size={size}")
    # Afficher le contenu des chunks INFO
    if chunk_id in ['LIST', 'INFO']:
        chunk_data = data[start+8:start+8+size]
        print(f"    Contenu (premier 200 octets): {chunk_data[:200]}")