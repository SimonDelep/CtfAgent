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

# Essayer LSB sur chaque canal séparément
def extract_lsb_bytes(samples):
    bits = [s & 1 for s in samples]
    bytes_data = []
    for i in range(0, len(bits), 8):
        if i+7 < len(bits):
            byte_val = 0
            for j in range(8):
                byte_val |= (bits[i+j] << j)
            bytes_data.append(byte_val)
    return bytes(bytes_data)

left_bytes = extract_lsb_bytes(samples_left)
right_bytes = extract_lsb_bytes(samples_right)

print("LSB Canal gauche (premières 50 bytes):")
print(left_bytes[:50])
print("LSB Canal droit (premières 50 bytes):")
print(right_bytes[:50])

# Essayer MSB (bit le plus significatif)
def extract_msb_bytes(samples):
    bits = [(s >> 15) & 1 for s in samples]  # Pour signed 16-bit, le bit 15 est le signe
    bytes_data = []
    for i in range(0, len(bits), 8):
        if i+7 < len(bits):
            byte_val = 0
            for j in range(8):
                byte_val |= (bits[i+j] << j)
            bytes_data.append(byte_val)
    return bytes(bytes_data)

left_msb = extract_msb_bytes(samples_left)
right_msb = extract_msb_bytes(samples_right)

print("\nMSB Canal gauche (premières 50 bytes):")
print(left_msb[:50])
print("MSB Canal droit (premières 50 bytes):")
print(right_msb[:50])