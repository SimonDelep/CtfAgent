import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Les échantillons sont stéréo, donc on a des paires (gauche, droite)
# Essayons de convertir chaque valeur d'échantillon en caractère ASCII
# Mais d'abord, regardons la distribution des valeurs

from collections import Counter
value_counts = Counter(samples)
print("Distribution des valeurs (top 20):")
for val, count in value_counts.most_common(20):
    print(f"  {val}: {count}")

print(f"\nValeurs minimales et maximales: {min(samples)} à {max(samples)}")

# Essayons de convertir les valeurs en ASCII directement
# Les valeurs semblent être très petites, donc peut-être qu'elles représentent des offsets ou des indices
# Ou peut-être qu'il faut les additionner par paires (stéréo)

# Option 1: Prendre uniquement le canal gauche (échantillons pairs)
left_channel = samples[::2]
right_channel = samples[1::2]

print(f"\nCanal gauche - min: {min(left_channel)}, max: {max(left_channel)}")
print(f"Canal droit - min: {min(right_channel)}, max: {max(right_channel)}")

# Essayons de convertir les valeurs en ASCII en ajoutant un offset
# Les valeurs ASCII imprimables vont de 32 à 126
# Si on ajoute 32 aux valeurs, on obtient des caractères imprimables

# Mais d'abord, cherchons des séquences qui pourraient former du texte
# Convertissons toutes les valeurs en caractères avec un offset
offset = 32
text = ''.join(chr((v + offset) % 256) for v in samples[:1000])
print(f"\nPremiers 1000 caractères avec offset 32: {repr(text[:200])}")