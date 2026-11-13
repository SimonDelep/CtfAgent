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

# Compter les valeurs
counter = Counter(all_values)
print("Distribution des valeurs:")
for val, count in sorted(counter.items()):
    print(f"  {val}: {count}")

# Trouver les valeurs uniques
print(f"\nValeurs uniques: {sorted(counter.keys())}")