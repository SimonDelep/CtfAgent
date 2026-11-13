import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
idx = data.find(b'data')
if idx != -1:
    # Taille des données audio
    data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
    print(f"Taille des données audio: {data_size}")
    
    # Les données audio commencent à idx+8
    audio_data = data[idx+8:idx+8+data_size]
    
    # C'est stéréo 16-bit, donc chaque échantillon est 2 octets, et il y a 2 canaux
    # Donc chaque "frame" est 4 octets (2 échantillons de 2 octets chacun)
    
    # Extraire tous les échantillons
    samples = []
    for i in range(0, len(audio_data), 4):
        if i+3 < len(audio_data):
            left = struct.unpack('<h', audio_data[i:i+2])[0]
            right = struct.unpack('<h', audio_data[i+2:i+4])[0]
            samples.append((left, right))
    
    print(f"Nombre de frames: {len(samples)}")
    
    # Afficher les premières frames
    for i in range(min(20, len(samples))):
        print(f"Frame {i}: left={samples[i][0]}, right={samples[i][1]}")