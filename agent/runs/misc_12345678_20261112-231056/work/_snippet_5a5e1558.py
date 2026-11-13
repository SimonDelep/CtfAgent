import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Extraire tous les échantillons
samples = []
for i in range(0, len(frames), 2):
    sample = struct.unpack('<h', frames[i:i+2])[0]
    samples.append(sample)

# Essayer 2 bits LSB
lsb2_bits = [(s & 3) for s in samples]  # 2 bits LSB
print(f"Premiers 20 valeurs 2 bits LSB: {lsb2_bits[:20]}")

# Regrouper par bytes (4 valeurs de 2 bits = 8 bits)
lsb2_bytes = []
for i in range(0, len(lsb2_bits) - 3, 4):
    byte_val = 0
    for j in range(4):
        byte_val |= (lsb2_bits[i + j] << (2 * j))  # LSB first
    lsb2_bytes.append(byte_val)

print(f"Premiers 50 bytes (2 bits LSB): {lsb2_bytes[:50]}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb2_bytes[:50])}")

# Chercher "csaw{"
target = b'csaw{'
for i in range(len(lsb2_bytes) - 4):
    if lsb2_bytes[i:i+5] == list(target):
        print(f"\nTrouvé 'csaw{{' à l'index {i}")
        start = max(0, i-5)
        end = min(len(lsb2_bytes), i+50)
        print(f"Message: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb2_bytes[start:end])}")
        break