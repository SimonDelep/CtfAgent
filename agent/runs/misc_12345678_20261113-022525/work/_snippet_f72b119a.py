import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
audio_data = data[data_start+8:data_start+8+6064208]

# Regarder les valeurs brutes - peut-être que certaines valeurs sont spéciales
# Cherchons des valeurs qui ne sont pas proches de 0
samples = []
for i in range(0, len(audio_data), 4):
    if i + 3 < len(audio_data):
        left = struct.unpack('<h', audio_data[i:i+2])[0]
        right = struct.unpack('<h', audio_data[i+2:i+4])[0]
        samples.append((left, right))

# Trouver les valeurs non nulles
non_zero = [(i, l, r) for i, (l, r) in enumerate(samples) if l != 0 or r != 0]
print(f"Nombre d'échantillons non nuls: {len(non_zero)}")
print(f"Total d'échantillons: {len(samples)}")

# Afficher les premiers échantillons non nuls
print("\nPremiers 50 échantillons non nuls (index, left, right):")
for idx, left, right in non_zero[:50]:
    print(f"  {idx}: left={left}, right={right}")

# Peut-être que les valeurs non nulles contiennent le message
# Extraire seulement les valeurs non nulles
values = []
for i, (l, r) in enumerate(samples):
    if l != 0:
        values.append(('L', l))
    if r != 0:
        values.append(('R', r))

print(f"\nNombre total de valeurs non nulles: {len(values)}")
print("Premières 100 valeurs:", values[:100])