import wave
import struct
import numpy as np

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    
# Convertir en échantillons 16-bit stéréo
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
print(f"Nombre total d'échantillons: {len(samples)}")

# Séparer les canaux (stéréo = 2 canaux)
left_channel = samples[0::2]
right_channel = samples[1::2]

print(f"Canal gauche: {len(left_channel)} échantillons")
print(f"Canal droit: {len(right_channel)} échantillons")

# Afficher quelques valeurs de chaque canal
print(f"Premiers 20 échantillons gauche: {left_channel[:20]}")
print(f"Premiers 20 échantillons droit: {right_channel[:20]}")

# Vérifier si un canal contient des données différentes
diff = sum(1 for l, r in zip(left_channel, right_channel) if l != r)
print(f"Nombre de différences entre canaux: {diff} sur {len(left_channel)}")