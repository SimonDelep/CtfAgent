import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
# Les données sont en stéréo, 16-bit little-endian
# Chaque échantillon est 2 bytes, et il y a 2 canaux
# Donc chaque "frame" contient 4 bytes (2 canaux * 2 bytes)

# Extraire tous les échantillons
samples = []
for i in range(0, len(frames), 2):
    sample = struct.unpack('<h', frames[i:i+2])[0]  # signed 16-bit little-endian
    samples.append(sample)

print(f"Nombre total d'échantillons: {len(samples)}")
print(f"Premiers 20 échantillons: {samples[:20]}")

# Extraire le LSB de chaque échantillon
lsb_bits = [s & 1 for s in samples]
print(f"Premiers 50 bits LSB: {''.join(map(str, lsb_bits[:50]))}")

# Regrouper par bytes (8 bits)
lsb_bytes = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)  # LSB first (bit 0 est le premier)
    lsb_bytes.append(byte_val)

print(f"Premiers 50 bytes LSB: {lsb_bytes[:50]}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes[:50])}")