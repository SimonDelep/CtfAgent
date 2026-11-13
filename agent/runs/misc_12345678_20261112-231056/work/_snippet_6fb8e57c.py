import wave
import struct

# Ouvrir le fichier WAV
with wave.open('12345678 (1).wav', 'rb') as wav:
    print(f"Nombre de canaux: {wav.getnchannels()}")
    print(f"Taille d'échantillon: {wav.getsampwidth()} bytes")
    print(f"Fréquence d'échantillonnage: {wav.getframerate()} Hz")
    print(f"Nombre de frames: {wav.getnframes()}")
    print(f"Durée: {wav.getnframes() / wav.getframerate():.2f} secondes")
    
    # Lire les frames
    frames = wav.readframes(wav.getnframes())
    print(f"Taille des données: {len(frames)} bytes")
    
    # Afficher les premiers bytes bruts
    print(f"Premiers 50 bytes: {frames[:50].hex()}")