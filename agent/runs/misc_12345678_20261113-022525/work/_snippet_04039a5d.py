import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]

# Mapping valeur absolue -> lettre (1=A, 2=B, etc.)
mapping1 = {i: chr(ord('A') + i - 1) for i in range(1, 9)}
text1 = ''.join(mapping1[abs(s)] for s in filtered)

# Analyser la fréquence des lettres
letter_counts = Counter(text1)
print("Fréquence des lettres (1=A, 2=B, etc.):")
total = len(text1)
for letter, cnt in sorted(letter_counts.items()):
    pct = cnt / total * 100
    print(f"  {letter}: {cnt} ({pct:.2f}%)")

# En anglais, E est la lettre la plus fréquente (~12.7%), puis T, A, O, I, N, S, H, R...
# Ici, A est la plus fréquente, donc peut-être que A = E dans le texte clair

# Essayons un décalage ROT sur le texte
print("\n\nEssais de décalage ROT:")
for shift in range(26):
    decoded = ''.join(chr((ord(c) - ord('A') + shift) % 26 + ord('A')) for c in text1[:100])
    print(f"ROT{shift}: {decoded}")
