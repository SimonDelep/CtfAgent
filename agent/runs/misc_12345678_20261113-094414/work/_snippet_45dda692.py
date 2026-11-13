import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    print(f"Nombre de canaux: {wav.getnchannels()}")
    print(f"Largeur d'échantillon: {wav.getsampwidth()}")
    print(f"Fréquence d'échantillonnage: {wav.getframerate()}")
    print(f"Nombre de frames: {wav.getnframes()}")
    print(f"Durée: {wav.getnframes() / wav.getframerate():.2f} secondes")
    
    # Lire les données
    data = wav.readframes(wav.getnframes())
    print(f"Taille des données: {len(data)} bytes")
    
    # Afficher les premiers bytes
    print(f"Premiers 100 bytes: {data[:100].hex()}")