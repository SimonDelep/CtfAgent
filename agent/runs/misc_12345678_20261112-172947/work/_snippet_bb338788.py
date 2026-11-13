import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    print("Nombre de canaux:", wav.getnchannels())
    print("Taille d'échantillon (bits):", wav.getsampwidth())
    print("Fréquence d'échantillonnage:", wav.getframerate())
    print("Nombre de frames:", wav.getnframes())
    print("Compression type:", wav.getcomptype())
    
    # Lire quelques échantillons
    frames = wav.readframes(100)
    print("Premiers bytes:", frames[:50].hex())