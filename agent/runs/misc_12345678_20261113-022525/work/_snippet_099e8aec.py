import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
audio_data = data[data_start+8:data_start+8+6064208]

# Essayer seulement le canal gauche (premier échantillon de chaque paire)
bits_left = []
for i in range(0, len(audio_data), 4):
    if i + 1 < len(audio_data):
        left = struct.unpack('<h', audio_data[i:i+2])[0]
        bits_left.append(left & 1)

print(f"Nombre de bits du canal gauche: {len(bits_left)}")

# Convertir en bytes
bytes_left = []
for i in range(0, len(bits_left) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (bits_left[i+j] << j)
    bytes_left.append(byte_val)

print("Canal gauche - premiers 100 bytes (hex):")
print(' '.join(f'{b:02x}' for b in bytes_left[:100]))

print("\nCanal gauche - ASCII:")
printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_left[:100])
print(printable)

# Essayer seulement le canal droit
bits_right = []
for i in range(0, len(audio_data), 4):
    if i + 3 < len(audio_data):
        right = struct.unpack('<h', audio_data[i+2:i+4])[0]
        bits_right.append(right & 1)

print(f"\nNombre de bits du canal droit: {len(bits_right)}")

bytes_right = []
for i in range(0, len(bits_right) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (bits_right[i+j] << j)
    bytes_right.append(byte_val)

print("Canal droit - premiers 100 bytes (hex):")
print(' '.join(f'{b:02x}' for b in bytes_right[:100]))

print("\nCanal droit - ASCII:")
printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_right[:100])
print(printable)