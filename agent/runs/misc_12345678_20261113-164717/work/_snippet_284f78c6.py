import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
idx = data.find(b'data')
data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+data_size]

# Extraire les échantillons
samples_left = []
samples_right = []

for i in range(0, len(audio_data), 4):
    if i+3 < len(audio_data):
        left = struct.unpack('<h', audio_data[i:i+2])[0]
        right = struct.unpack('<h', audio_data[i+2:i+4])[0]
        samples_left.append(left)
        samples_right.append(right)

# Regarder la différence entre les canaux
diffs = []
for i in range(len(samples_left)):
    diff = samples_left[i] - samples_right[i]
    diffs.append(diff)

# Extraire LSB de la différence
bits = [d & 1 for d in diffs]
bytes_data = []
for i in range(0, len(bits), 8):
    if i+7 < len(bits):
        byte_val = 0
        for j in range(8):
            byte_val |= (bits[i+j] << j)
        bytes_data.append(byte_val)

print("LSB de la différence entre canaux (premières 100 bytes):")
print(bytes(bytes_data[:100]))

# Essayer aussi la somme
sums = []
for i in range(len(samples_left)):
    s = samples_left[i] + samples_right[i]
    sums.append(s)

bits = [s & 1 for s in sums]
bytes_data = []
for i in range(0, len(bits), 8):
    if i+7 < len(bits):
        byte_val = 0
        for j in range(8):
            byte_val |= (bits[i+j] << j)
        bytes_data.append(byte_val)

print("\nLSB de la somme des canaux (premières 100 bytes):")
print(bytes(bytes_data[:100]))