import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    # Taille du chunk data
    chunk_size = struct.unpack('<I', data[data_start+4:data_start+8])[0]
    print(f"Chunk data trouvé à offset {data_start}, taille {chunk_size}")
    
    # Les données audio commencent après le header de 8 octets (4 pour 'data', 4 pour la taille)
    audio_data = data[data_start+8:data_start+8+chunk_size]
    print(f"Longueur des données audio: {len(audio_data)} octets")
    
    # C'est du PCM 16-bit stéréo, donc 2 canaux x 2 octets = 4 octets par échantillon
    num_samples = len(audio_data) // 4
    print(f"Nombre d'échantillons (stéréo): {num_samples}")
    
    # Afficher les premiers échantillons
    print("\nPremiers échantillons (gauche, droite):")
    for i in range(min(20, num_samples)):
        offset = i * 4
        left = struct.unpack('<h', audio_data[offset:offset+2])[0]
        right = struct.unpack('<h', audio_data[offset+2:offset+4])[0]
        print(f"  {i}: left={left}, right={right}")