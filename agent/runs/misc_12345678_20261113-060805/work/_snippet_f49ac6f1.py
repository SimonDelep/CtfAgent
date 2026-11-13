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
    
    # Combiner les deux canaux
    all_samples = samples_left + samples_right
    
    # Regardons les valeurs qui sont dans la plage ASCII imprimable (32-126)
    # Et voyons si elles forment un message
    ascii_chars = []
    for s in all_samples:
        if 32 <= s <= 126:
            ascii_chars.append(chr(s))
    
    print(f"Nombre de caractères ASCII trouvés: {len(ascii_chars)}")
    print("Premiers 200 caractères:")
    print(''.join(ascii_chars[:200]))
    
    # Regardons aussi les valeurs qui pourraient être des caractères spéciaux
    # Peut-être que le message est caché dans les valeurs > 100
    high_values = [s for s in all_samples if s > 100]
    print(f"\nNombre de valeurs > 100: {len(high_values)}")
    print("Premières 50 valeurs > 100:")
    print(high_values[:50])