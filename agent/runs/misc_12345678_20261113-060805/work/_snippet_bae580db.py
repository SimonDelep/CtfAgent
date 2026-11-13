import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8
    audio_data = data[data_start:]
    
    # Extraire tous les échantillons
    samples_left = []
    samples_right = []
    for i in range(0, len(audio_data), 4):
        if i + 4 <= len(audio_data):
            left = struct.unpack('<h', audio_data[i:i+2])[0]
            right = struct.unpack('<h', audio_data[i+2:i+4])[0]
            samples_left.append(left)
            samples_right.append(right)
    
    # Le titre "12345678" pourrait indiquer qu'il faut prendre les échantillons
    # aux positions 1, 2, 3, 4, 5, 6, 7, 8, 9, 10... (en comptant à partir de 1)
    # ou peut-être que c'est une séquence de 8 caractères
    
    # Essayons de voir si les valeurs des échantillons correspondent à des caractères
    # en utilisant uniquement les valeurs positives
    positive_left = [s for s in samples_left if s > 0]
    positive_right = [s for s in samples_right if s > 0]
    
    print(f"Nombre d'échantillons positifs gauche: {len(positive_left)}")
    print(f"Nombre d'échantillons positifs droite: {len(positive_right)}")
    
    # Regardons les premières valeurs positives
    print("\nPremières 100 valeurs positives (gauche):")
    print(positive_left[:100])
    
    # Essayons de convertir ces valeurs en caractères
    chars = [chr(s) if 32 <= s <= 126 else '?' for s in positive_left[:200]]
    print("\nCaractères (valeurs positives gauche):")
    print(''.join(chars[:200]))