import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Décoder comme signed 16-bit little-endian
samples = []
for i in range(0, len(data), 2):
    if i + 1 < len(data):
        sample = struct.unpack('<h', data[i:i+2])[0]
        samples.append(sample)

# Extraire le LSB de chaque échantillon
lsb_bits = [abs(s) & 1 for s in samples]

# Convertir en bytes
lsb_bytes = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << (7 - j))
    lsb_bytes.append(byte_val)

# Afficher en ASCII
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes[:300])
print("LSB des échantillons:")
print(result)
print()
print("Premiers 50 bytes LSB:", lsb_bytes[:50])