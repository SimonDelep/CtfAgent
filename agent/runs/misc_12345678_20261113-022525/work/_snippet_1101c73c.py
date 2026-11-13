import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]

# Regardons la séquence des signes uniquement
signs = [1 if s > 0 else 0 for s in filtered]

# Compter les transitions de signe
transitions = 0
for i in range(len(signs) - 1):
    if signs[i] != signs[i+1]:
        transitions += 1

print(f"Nombre de transitions de signe: {transitions}")
print(f"Total de symboles: {len(signs)}")
print(f"Pourcentage de transitions: {transitions/len(signs)*100:.2f}%")

# Peut-être que le message est encodé dans les séquences de signes identiques
# Par exemple, une séquence de n signes positifs suivie de m signes négatifs encode quelque chose

# Regardons les longueurs des séquences de signes identiques
seq_lengths = []
current_len = 1
for i in range(1, len(signs)):
    if signs[i] == signs[i-1]:
        current_len += 1
    else:
        seq_lengths.append((signs[i-1], current_len))
        current_len = 1
seq_lengths.append((signs[-1], current_len))

print(f"\nNombre de séquences de signes identiques: {len(seq_lengths)}")

# Afficher les premières séquences
print("Premières séquences (signe, longueur):")
for i, (sgn, length) in enumerate(seq_lengths[:30]):
    print(f"  {sgn}: {length}")

# Compter la distribution des longueurs
length_counts = Counter(length for sgn, length in seq_lengths)
print("\nDistribution des longueurs de séquences:")
for length, cnt in sorted(length_counts.items())[:20]:
    print(f"  longueur {length}: {cnt}")
