import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
    # C'est stéréo, donc chaque échantillon est 2 bytes (16 bits)
    # Essayons d'extraire les LSB de chaque échantillon (pas de chaque byte)
    
    # Convertir en échantillons 16-bit
    samples = []
    for i in range(0, len(frames), 2):
        if i + 1 < len(frames):
            sample = frames[i] | (frames[i+1] << 8)
            samples.append(sample)
    
    print("Nombre d'échantillons:", len(samples))
    
    # Extraire le LSB de chaque échantillon
    lsb_bits = [s & 1 for s in samples]
    
    # Convertir en bytes
    lsb_bytes = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | lsb_bits[i + j]
        lsb_bytes.append(byte_val)
    
    result = bytes(lsb_bytes[:300])
    print("LSB des échantillons (hex):", result[:60].hex())
    print("LSB des échantillons (ascii):", result)