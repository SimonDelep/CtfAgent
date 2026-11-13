import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    n_frames = wf.getnframes()
    
    # Lire les données brutes
    data = wf.readframes(n_frames)
    
    # Extraire les échantillons par canal
    # Pour stéréo, les échantillons sont interleaved: L, R, L, R, ...
    left_samples = []
    right_samples = []
    
    for i in range(0, len(data), sampwidth * 2):
        left = int.from_bytes(data[i:i+sampwidth], byteorder='little', signed=True)
        right = int.from_bytes(data[i+sampwidth:i+sampwidth*2], byteorder='little', signed=True)
        left_samples.append(left)
        right_samples.append(right)
    
    print(f"Left samples count: {len(left_samples)}")
    print(f"Right samples count: {len(right_samples)}")
    
    # Extraire LSB du canal gauche
    lsb_left = [s & 1 for s in left_samples]
    
    # Convertir en bytes (LSB first)
    bytes_left = []
    for i in range(0, len(lsb_left) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_left[i + j] << j)
        bytes_left.append(byte_val)
    
    text_left = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_left[:100])
    print(f"Left channel LSB text: {text_left}")
    
    # Extraire LSB du canal droit
    lsb_right = [s & 1 for s in right_samples]
    
    bytes_right = []
    for i in range(0, len(lsb_right) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_right[i + j] << j)
        bytes_right.append(byte_val)
    
    text_right = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_right[:100])
    print(f"Right channel LSB text: {text_right}")
