import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    print("Nombre de canaux:", wav.getnchannels())
    print("Taille d'échantillon (bytes):", wav.getsampwidth())
    print("Fréquence d'échantillonnage:", wav.getframerate())
    print("Nombre de frames:", wav.getnframes())
    print("Durée (s):", wav.getnframes() / wav.getframerate())
    
    # Lire les frames
    frames = wav.readframes(wav.getnframes())
    print("Taille des données:", len(frames), "bytes")
    
    # Déterminer le format
    n_channels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    
    # Convertir en samples
    if sampwidth == 2:
        fmt = '<' + 'h' * n_channels  # little-endian signed short
        samples = struct.unpack(fmt * (len(frames) // (sampwidth * n_channels)), frames)
        print("Nombre total de samples:", len(samples))
        print("Premiers 20 samples:", samples[:20])