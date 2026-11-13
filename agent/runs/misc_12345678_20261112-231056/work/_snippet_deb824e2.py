import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Données stéréo: chaque frame contient 2 échantillons (gauche, droit)
# Extraire les canaux séparément
left_samples = []
right_samples = []

for i in range(0, len(frames), 4):  # 4 bytes par frame (2 canaux * 2 bytes)
    if i + 3 < len(frames):
        left = struct.unpack('<h', frames[i:i+2])[0]
        right = struct.unpack('<h', frames[i+2:i+4])[0]
        left_samples.append(left)
        right_samples.append(right)

print(f"Nombre d'échantillons par canal: {len(left_samples)}")

# Extraire LSB du canal gauche
left_lsb_bits = [s & 1 for s in left_samples]
left_lsb_bytes = []
for i in range(0, len(left_lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (left_lsb_bits[i + j] << (7 - j))  # MSB first
    left_lsb_bytes.append(byte_val)

print("Canal gauche (MSB first):")
print(f"Premiers 50 bytes: {left_lsb_bytes[:50]}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in left_lsb_bytes[:50])}")

# Extraire LSB du canal droit
right_lsb_bits = [s & 1 for s in right_samples]
right_lsb_bytes = []
for i in range(0, len(right_lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (right_lsb_bits[i + j] << (7 - j))  # MSB first
    right_lsb_bytes.append(byte_val)

print("\nCanal droit (MSB first):")
print(f"Premiers 50 bytes: {right_lsb_bytes[:50]}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in right_lsb_bytes[:50])}")