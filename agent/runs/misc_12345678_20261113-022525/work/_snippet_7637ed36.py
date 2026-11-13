import struct
from collections import Counter

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
audio_data = data[data_start+8:data_start+8+6064208]

# Extraire toutes les valeurs
all_values = []
for i in range(0, len(audio_data), 4):
    if i + 3 < len(audio_data):
        left = struct.unpack('<h', audio_data[i:i+2])[0]
        right = struct.unpack('<h', audio_data[i+2:i+4])[0]
        all_values.append(left)
        all_values.append(right)

# Compter les valeurs les plus fréquentes
counter = Counter(all_values)
print("Valeurs les plus fréquentes:")
for val, count in counter.most_common(50):
    print(f"  {val}: {count}")

# Regardons les valeurs entre -10 et 10
small_values = [v for v in all_values if -10 <= v <= 10]
print(f"\nNombre de valeurs entre -10 et 10: {len(small_values)}")
print(f"Total de valeurs: {len(all_values)}")
print(f"Pourcentage: {100*len(small_values)/len(all_values):.2f}%")

# Compter les petites valeurs
small_counter = Counter(small_values)
print("\nDistribution des petites valeurs:")
for val in range(-10, 11):
    if val in small_counter:
        print(f"  {val}: {small_counter[val]}")