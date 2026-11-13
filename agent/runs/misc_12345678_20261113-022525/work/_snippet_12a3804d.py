import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]
print(f"Nombre d'échantillons avec |valeur| entre 1 et 8: {len(filtered)}")
print(f"Total échantillons: {len(samples)}")
print(f"Pourcentage: {len(filtered)/len(samples)*100:.2f}%")

# Compter les valeurs positives et négatives
pos = [s for s in filtered if s > 0]
neg = [s for s in filtered if s < 0]
print(f"Positifs: {len(pos)}, Négatifs: {len(neg)}")

# Distribution par valeur
counts = Counter(filtered)
print("\nDistribution des valeurs:")
for v in sorted(counts.keys()):
    print(f"  {v}: {counts[v]}")
