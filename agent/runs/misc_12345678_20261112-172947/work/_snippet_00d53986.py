import wave
import struct
import math

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    
# Convertir en échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Séparer les canaux
left_channel = samples[0::2]
right_channel = samples[1::2]

# Calculer l'amplitude moyenne par canal
left_avg = sum(abs(s) for s in left_channel) / len(left_channel)
right_avg = sum(abs(s) for s in right_channel) / len(right_channel)

print(f"Amplitude moyenne canal gauche: {left_avg:.2f}")
print(f"Amplitude moyenne canal droit: {right_avg:.2f}")

# Vérifier si un canal est silencieux
print(f"\nNombre de zéros exacts:")
print(f"  Canal gauche: {left_channel.count(0)}")
print(f"  Canal droit: {right_channel.count(0)}")

# Vérifier les valeurs non nulles
left_nonzero = [s for s in left_channel if s != 0]
right_nonzero = [s for s in right_channel if s != 0]
print(f"\nNombre de valeurs non nulles:")
print(f"  Canal gauche: {len(left_nonzero)}")
print(f"  Canal droit: {len(right_nonzero)}")

# Si un canal a beaucoup de zéros, peut-être que l'autre contient le message
if len(left_nonzero) < len(right_nonzero):
    print("\nLe canal gauche a moins de données non nulles - peut-être le message est là ?")
else:
    print("\nLe canal droit a plus de données non nulles")

# Regardons les valeurs non nulles du canal qui a le moins de zéros
# Peut-être que c'est du LSB dans les valeurs non nulles