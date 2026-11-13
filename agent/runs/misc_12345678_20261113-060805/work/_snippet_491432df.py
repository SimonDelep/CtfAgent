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
    
    # Essayons de prendre les échantillons aux positions 1, 2, 3, 4, 5, 6, 7, 8...
    # Le titre est "12345678" - peut-être qu'il faut prendre les échantillons à ces positions
    # ou peut-être que c'est une séquence de 8 échantillons qui contient le message
    
    # Regardons les échantillons aux positions 1, 2, 3, 4, 5, 6, 7, 8 (indices 0-7)
    print("Échantillons aux positions 0-7:")
    for i in range(8):
        print(f"  Position {i}: gauche={samples_left[i]}, droite={samples_right[i]}")
    
    # Peut-être que le message est dans les valeurs absolues
    print("\nValeurs absolues des premiers 20 échantillons (canal gauche):")
    print([abs(s) for s in samples_left[:20]])
    
    # Essayons de voir si les valeurs absolues forment des caractères
    abs_values = [abs(s) for s in samples_left]
    ascii_from_abs = [chr(v) if 32 <= v <= 126 else '.' for v in abs_values[:200]]
    print("\nCaractères à partir des valeurs absolues (canal gauche):")
    print(''.join(ascii_from_abs[:200]))