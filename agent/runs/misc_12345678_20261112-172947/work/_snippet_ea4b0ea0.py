import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    
# Convertir en échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Trouver toutes les séquences de zéros (min_len=6 pour éviter le bruit)
def find_zero_sequences(samples, min_len=6):
    sequences = []
    current_len = 0
    current_start = 0
    for i, s in enumerate(samples):
        if s == 0:
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            if current_len >= min_len:
                sequences.append((current_start, current_len))
            current_len = 0
    if current_len >= min_len:
        sequences.append((current_start, current_len))
    return sequences

all_zeros = find_zero_sequences(samples, min_len=6)

print(f"Total de séquences de zéros (>= 6): {len(all_zeros)}")

# Extraire les longueurs
lengths = [l for _, l in all_zeros]
print(f"Longueurs: {lengths[:50]}")

# Compter les occurrences de chaque longueur
from collections import Counter
counts = Counter(lengths)
print(f"\nComptage des longueurs:")
for length, count in sorted(counts.items()):
    print(f"  {length}: {count}")

# Essayer de mapper les longueurs à des caractères
# Peut-être que 6=point, 7=trait, ou quelque chose comme ça
# Ou peut-être que les longueurs encodent directement des valeurs ASCII

# Vérifions si les longueurs pourraient être des codes ASCII
print("\nValeurs ASCII possibles:")
for l in set(lengths):
    print(f"  {l} -> chr({l}) = {chr(l) if 32 <= l < 127 else 'non imprimable'}")