import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    n_channels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    n_frames = wav.getnframes()
    
    # Lire les frames
    frames = wav.readframes(n_frames)
    
    # Pour stéréo 16-bit, chaque frame a 2 samples (gauche, droite)
    # Total samples = n_frames * n_channels
    total_samples = n_frames * n_channels
    
    # Déballer comme signed short (2 bytes)
    fmt = '<' + 'h' * total_samples
    samples = struct.unpack(fmt, frames)
    
    print("Nombre total de samples:", len(samples))
    print("Premiers 20 samples:", samples[:20])
    
    # Séparer canaux gauche et droit
    left = samples[0::2]
    right = samples[1::2]
    print("Samples gauche (premiers 10):", left[:10])
    print("Samples droit (premiers 10):", right[:10])