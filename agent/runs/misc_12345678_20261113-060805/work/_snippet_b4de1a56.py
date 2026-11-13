import wave
import struct

# Ouvrir le fichier wav
with wave.open('audio.wav', 'rb') as wav:
    print(f"Nombre de canaux: {wav.getnchannels()}")
    print(f"Taille d'échantillon: {wav.getsampwidth()} bytes")
    print(f"Fréquence d'échantillonnage: {wav.getframerate()} Hz")
    print(f"Nombre de frames: {wav.getnframes()}")
    print(f"Durée: {wav.getnframes() / wav.getframerate():.2f} secondes")
    
    # Lire quelques échantillons pour inspection
    frames = wav.readframes(100)
    # Stéréo, 2 bytes par échantillon
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    print(f"\nPremiers 20 échantillons (canal gauche):")
    print([samples[i] for i in range(0, len(samples), 2)][:20])
    print(f"\nPremiers 20 échantillons (canal droit):")
    print([samples[i] for i in range(1, len(samples), 2)][:20])