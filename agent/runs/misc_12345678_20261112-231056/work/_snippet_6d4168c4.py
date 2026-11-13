import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    
    print(f"Channels: {n_channels}")
    print(f"Sample width: {sampwidth} bytes")
    print(f"Frame rate: {framerate} Hz")
    print(f"Number of frames: {n_frames}")
    print(f"Total samples: {n_frames * n_channels}")
    
    # Lire les données brutes
    data = wf.readframes(n_frames)
    print(f"Data length: {len(data)} bytes")
    
    # Extraire les échantillons
    samples = []
    for i in range(0, len(data), sampwidth):
        sample = int.from_bytes(data[i:i+sampwidth], byteorder='little', signed=True)
        samples.append(sample)
    
    print(f"First 20 samples: {samples[:20]}")
    
    # Extraire LSB de chaque échantillon
    lsb_bits = [s & 1 for s in samples]
    
    # Convertir en bytes (8 bits par byte)
    bytes_from_lsb = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)  # bit 0 en premier (LSB first)
        bytes_from_lsb.append(byte_val)
    
    # Afficher les premiers bytes comme texte
    text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_from_lsb[:100])
    print(f"LSB text (LSB first): {text}")
    
    # Tenter MSB first
    bytes_msb = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << (7-j))  # MSB first
        bytes_msb.append(byte_val)
    
    text_msb = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_msb[:100])
    print(f"LSB text (MSB first): {text_msb}")
