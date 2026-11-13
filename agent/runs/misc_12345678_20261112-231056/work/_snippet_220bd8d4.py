import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    params = wav.getparams()
    print(f"Nombre de canaux: {params.nchannels}")
    print(f"Échantillons par seconde: {params.framerate}")
    print(f"Échantillons par bloc: {params.sampwidth}")
    print(f"Nombre d'échantillons: {params.nframes}")
    
    # Lire les données brutes
    data = wav.readframes(params.nframes)
    print(f"Longueur des données: {len(data)} bytes")
    
    # Afficher les premiers bytes
    print("Premiers 100 bytes:", list(data[:100]))
    
    # Afficher les derniers bytes
    print("Derniers 50 bytes:", list(data[-50:]))