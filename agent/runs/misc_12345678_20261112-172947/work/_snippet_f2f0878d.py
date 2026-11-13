import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
    # Convertir en échantillons 16-bit
    samples = []
    for i in range(0, len(frames), 2):
        if i + 1 < len(frames):
            sample = frames[i] | (frames[i+1] << 8)
            # Convertir en signed 16-bit
            if sample >= 32768:
                sample -= 65536
            samples.append(sample)
    
    # Regarder les valeurs uniques ou les motifs
    print("Nombre d'échantillons:", len(samples))
    print("Valeurs minimales et maximales:", min(samples), max(samples))
    
    # Chercher des séquences de valeurs nulles ou constantes
    zero_runs = []
    current_run = 0
    for s in samples:
        if s == 0:
            current_run += 1
        else:
            if current_run > 10:
                zero_runs.append(current_run)
            current_run = 0
    if current_run > 10:
        zero_runs.append(current_run)
    
    print("Longueurs des séquences de zéros (>10):", zero_runs[:20])