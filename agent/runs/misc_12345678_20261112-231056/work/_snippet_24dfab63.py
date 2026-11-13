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

# LSB first
lsb_bytes = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)
    lsb_bytes.append(byte_val)

# Chercher toutes les occurrences de '{' (ASCII 123)
for i, b in enumerate(lsb_bytes):
    if b == 123:  # '{'
        print(f"Trouvé '{{' à l'index {i}")
        # Afficher 100 bytes autour
        start = max(0, i-10)
        end = min(len(lsb_bytes), i+100)
        msg = lsb_bytes[start:end]
        ascii_msg = ''.join(chr(b) if 32 <= b < 127 else '.' for b in msg)
        print(f"Contexte: {ascii_msg}")
        print()