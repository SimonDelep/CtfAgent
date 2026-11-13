import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Trouver les valeurs uniques et leurs fréquences
counts = Counter(samples)

# Regrouper par valeur absolue
abs_counts = Counter()
for v, c in counts.items():
    abs_counts[abs(v)] += c

# Afficher les 20 valeurs absolues les plus fréquentes
print("Top 20 valeurs absolues par fréquence:")
for val, cnt in abs_counts.most_common(20):
    print(f"  |{val}|: {cnt}")

# Vérifier si certaines valeurs absolues dominent
total = sum(abs_counts.values())
print(f"\nTotal échantillons: {total}")

# Afficher les valeurs absolues les plus fréquentes avec leurs pourcentages
print("\nPourcentages des valeurs absolues les plus fréquentes:")
for val, cnt in abs_counts.most_common(16):
    pct = cnt / total * 100
    print(f"  |{val}|: {cnt} ({pct:.2f}%)")
