import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
audio_data = data[data_start+8:data_start+8+6064208]

# Extraire toutes les valeurs dans l'ordre
all_values = []
for i in range(0, len(audio_data), 4):
    if i + 3 < len(audio_data):
        left = struct.unpack('<h', audio_data[i:i+2])[0]
        right = struct.unpack('<h', audio_data[i+2:i+4])[0]
        all_values.append(left)
        all_values.append(right)

# Regardons seulement les valeurs positives (1-8)
positive_values = [v for v in all_values if 1 <= v <= 8]
print(f"Nombre de valeurs positives entre 1 et 8: {len(positive_values)}")
print("Premières 200 valeurs positives:", positive_values[:200])

# Peut-être que chaque valeur positive représente un caractère
# Essayons de mapper 1->A, 2->B, etc.
mapped = ''.join(chr(ord('A') + v - 1) for v in positive_values[:100])
print("\nMappé (1->A, 2->B, etc.):", mapped)

# Ou peut-être que c'est juste les chiffres
print("\nComme chaîne:", ''.join(str(v) for v in positive_values[:100]))