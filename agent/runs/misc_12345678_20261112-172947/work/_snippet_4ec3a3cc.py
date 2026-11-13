import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
    # Séparer les canaux gauche et droit
    # Stéréo: échantillon gauche, échantillon droit, échantillon gauche, ...
    # Chaque échantillon est 2 bytes
    
    left_samples = []
    right_samples = []
    
    for i in range(0, len(frames), 4):
        if i + 3 < len(frames):
            # Échantillon gauche
            left = frames[i] | (frames[i+1] << 8)
            left_samples.append(left)
            # Échantillon droit
            right = frames[i+2] | (frames[i+3] << 8)
            right_samples.append(right)
    
    print("Nombre d'échantillons par canal:", len(left_samples))
    
    # Extraire les LSB du canal gauche
    lsb_left = [s & 1 for s in left_samples]
    lsb_bytes_left = []
    for i in range(0, len(lsb_left) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | lsb_left[i + j]
        lsb_bytes_left.append(byte_val)
    
    result_left = bytes(lsb_bytes_left[:200])
    print("LSB canal gauche (ascii):", result_left)
    
    # Extraire les LSB du canal droit
    lsb_right = [s & 1 for s in right_samples]
    lsb_bytes_right = []
    for i in range(0, len(lsb_right) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | lsb_right[i + j]
        lsb_bytes_right.append(byte_val)
    
    result_right = bytes(lsb_bytes_right[:200])
    print("LSB canal droit (ascii):", result_right)