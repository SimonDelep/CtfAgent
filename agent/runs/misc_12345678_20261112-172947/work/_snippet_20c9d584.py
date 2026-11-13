import struct
from collections import Counter

with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'data')
data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+data_size]

num_samples = len(audio_data) // 4

# Extraire le canal droit
right_samples = []
for i in range(num_samples):
    offset = i * 4
    right = struct.unpack('<h', audio_data[offset+2:offset+4])[0]
    right_samples.append(right)

# Trouver les séquences de zéros dans l'ordre
def find_zero_sequences_ordered(samples):
    sequences = []
    current_len = 0
    for s in samples:
        if s == 0:
            current_len += 1
        else:
            if current_len > 0:
                sequences.append(current_len)
            current_len = 0
    if current_len > 0:
        sequences.append(current_len)
    return sequences

right_zero_seqs = find_zero_sequences_ordered(right_samples)

# Peut-être que les séquences longues (>= 8 ou >= 10) sont des séparateurs entre lettres/mots
# Et les courtes sont des points/traits

# Regardons la distribution des longueurs
counter = Counter(right_zero_seqs)
print("Distribution des longueurs:")
for length in sorted(counter.keys()):
    print(f"  {length}: {counter[length]}")

# Hypothèse: longueurs <= 5 = point, 6-10 = trait, > 10 = séparateur
# Ou peut-être: 1-3 = point, 4-6 = trait, > 6 = séparateur

# Essayons de mapper:
# Si on considère que les séquences de zéros sont les ESPACES entre les sons
# Et que la durée de l'espace encode quelque chose

# Autre approche: peut-être que les séquences de zéros DE LONGUEUR SPÉCIFIQUE
# représentent des symboles Morse

# Regardons les séquences de longueur >= 8 (potentiels séparateurs)
long_seqs = [i for i, seq in enumerate(right_zero_seqs) if seq >= 8]
print(f"\nIndices des séquences >= 8: {long_seqs[:20]}")
print(f"Nombre de séquences >= 8: {len(long_seqs)}")

# Peut-être que chaque séquence de zéros représente un symbole, et sa longueur
# détermine si c'est un point ou un trait