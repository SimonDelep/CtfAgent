import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    n_channels = wav.getnchannels()
    sample_width = wav.getsampwidth()
    framerate = wav.getframerate()
    n_frames = wav.getnframes()
    
    print(f"Channels: {n_channels}, Sample width: {sample_width}, Frame rate: {framerate}, Frames: {n_frames}")
    
    # Lire tous les échantillons
    raw_data = wav.readframes(n_frames)
    
    if sample_width == 2:
        samples = struct.unpack(f'{n_frames * n_channels}h', raw_data)
    elif sample_width == 1:
        samples = struct.unpack(f'{n_frames * n_channels}B', raw_data)
    else:
        print(f"Sample width {sample_width} non géré")
        samples = []
    
    print(f"Nombre total d'échantillons: {len(samples)}")
    
    # Extraire les valeurs uniques
    unique_vals = sorted(set(samples))
    print(f"Valeurs uniques: {unique_vals}")
    
    # Compter les occurrences
    from collections import Counter
    counts = Counter(samples)
    print("\nFréquences des valeurs:")
    for v in sorted(counts.keys()):
        print(f"  {v}: {counts[v]}")
