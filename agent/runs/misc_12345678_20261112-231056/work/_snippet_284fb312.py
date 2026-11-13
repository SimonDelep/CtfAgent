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

# Extraire le LSB de chaque échantillon
lsb_bits = [s & 1 for s in samples]

# Essayer LSB first (bit 0 est le premier byte, bit 7 est le dernier)
lsb_bytes_lsb_first = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)  # LSB first
    lsb_bytes_lsb_first.append(byte_val)

print("LSB first (bit 0 en premier):")
print(f"Premiers 50 bytes: {lsb_bytes_lsb_first[:50]}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes_lsb_first[:50])}")

# Chercher "csaw{"
target = b'csaw{'
for i in range(len(lsb_bytes_lsb_first) - 4):
    if lsb_bytes_lsb_first[i:i+5] == list(target):
        print(f"\nTrouvé 'csaw{{' à l'index {i}")
        # Afficher plus de contexte
        start = max(0, i-5)
        end = min(len(lsb_bytes_lsb_first), i+50)
        print(f"Message: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes_lsb_first[start:end])}")
        break