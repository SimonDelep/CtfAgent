import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())

# Extraire les canaux
left_samples = []
right_samples = []

for i in range(0, len(data), 4):
    if i + 3 < len(data):
        left_val = int.from_bytes(data[i:i+2], 'little', signed=True)
        right_val = int.from_bytes(data[i+2:i+4], 'little', signed=True)
        left_samples.append(left_val)
        right_samples.append(right_val)

# Essayer LSB sur le canal droit
lsb_bits = []
for v in right_samples:
    lsb_bits.append(abs(v) & 1)

# Convertir en bytes
bytes_from_lsb = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)
    bytes_from_lsb.append(byte_val)

# Afficher les premiers bytes comme ASCII
print("LSB bytes (first 100):")
print(bytes(bytes_from_lsb[:100]))

# Essayer aussi le canal gauche
lsb_bits_left = [abs(v) & 1 for v in left_samples]
bytes_from_lsb_left = []
for i in range(0, len(lsb_bits_left) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits_left[i + j] << j)
    bytes_from_lsb_left.append(byte_val)

print("\nLSB left bytes (first 100):")
print(bytes(bytes_from_lsb_left[:100]))

# Essayer la différence entre canaux
diff_samples = [left_samples[i] - right_samples[i] for i in range(len(left_samples))]
lsb_bits_diff = [abs(v) & 1 for v in diff_samples]
bytes_from_lsb_diff = []
for i in range(0, len(lsb_bits_diff) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits_diff[i + j] << j)
    bytes_from_lsb_diff.append(byte_val)

print("\nLSB diff bytes (first 100):")
print(bytes(bytes_from_lsb_diff[:100]))