import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    print(f"Nombre de canaux: {wav.getnchannels()}")
    print(f"Largeur d'échantillon: {wav.getsampwidth()} bytes")
    print(f"Fréquence d'échantillonnage: {wav.getframerate()} Hz")
    print(f"Nombre de frames: {wav.getnframes()}")
    print(f"Durée: {wav.getnframes() / wav.getframerate():.2f} secondes")
    
    # Lire les données
    data = wav.readframes(wav.getnframes())
    print(f"Taille des données: {len(data)} bytes")
    
    # Afficher les premiers échantillons
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
    print(f"Premiers 50 échantillons: {samples[:50]}")