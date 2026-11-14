# Analyser la structure du fichier WAV et extraire les chunks
with open('audio.wav', 'rb') as f:
    data = f.read()

# RIFF header
print("RIFF header:")
print(f"  Signature: {data[0:4]}")
print(f"  Taille: {int.from_bytes(data[4:8], 'little')}")
print(f"  Format: {data[8:12]}")

# Chercher les chunks
pos = 12
while pos < len(data):
    chunk_id = data[pos:pos+4]
    if len(chunk_id) < 4:
        break
    try:
        chunk_size = int.from_bytes(data[pos+4:pos+8], 'little')
    except:
        break
    
    chunk_data = data[pos+8:pos+8+chunk_size]
    
    if chunk_id in [b'fmt ', b'data', b'LIST', b'ID3 ']:
        print(f"\nChunk {chunk_id}: taille={chunk_size}")
        if chunk_id == b'LIST':
            # LIST contient souvent INFO
            print(f"  Type: {chunk_data[:4]}")
            # Afficher les strings dans LIST
            import re
            strings = re.findall(rb'[\x20-\x7e]{4,}', chunk_data)
            for s in strings[:10]:
                print(f"    String: {s}")
        elif chunk_id == b'ID3 ':
            print(f"  ID3 version: {chunk_data[4:7]}")
            # Afficher le contenu
            print(f"  Début du payload: {chunk_data[10:50]}")
            # Chercher des strings
            import re
            strings = re.findall(rb'[\x20-\x7e]{4,}', chunk_data)
            for s in strings[:20]:
                print(f"    String: {s}")
        elif chunk_id == b'fmt ':
            print(f"  Format info: {chunk_data[:20]}")
        elif chunk_id == b'data':
            print(f"  Données audio: {chunk_size} octets")
    
    # Avancer au prochain chunk (aligné sur 2 octets)
    pos += 8 + chunk_size
    if chunk_size % 2 == 1:
        pos += 1