import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    print(f"Nombre de canaux: {wav.getnchannels()}")
    print(f"Taille d'échantillon: {wav.getsampwidth()} bytes")
    print(f"Fréquence d'échantillonnage: {wav.getframerate()} Hz")
    print(f"Nombre de frames: {wav.getnframes()}")
    print(f"Durée: {wav.getnframes() / wav.getframerate():.2f} secondes")
    
    # Lire les données brutes
    frames = wav.readframes(wav.getnframes())
    print(f"Taille des données: {len(frames)} bytes")
    
    # Afficher les premiers échantillons
    if wav.getsampwidth() == 2:
        samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
        print(f"Nombre d'échantillons: {len(samples)}")
        print("Premiers 50 échantillons:", samples[:50])
        print("Derniers 50 échantillons:", samples[-50:])