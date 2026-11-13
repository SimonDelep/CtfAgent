import wave
import struct

# Ouvrir le fichier wav
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
# Stéréo, 2 bytes par échantillon
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Extraire LSB de chaque échantillon (canal gauche uniquement d'abord)
lsb_bits = [samples[i] & 1 for i in range(0, len(samples), 2)]

# Convertir en bytes (8 bits par caractère)
bytes_data = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)
    bytes_data.append(byte_val)

# Afficher les premiers bytes en ASCII
print("LSB canal gauche - premiers 200 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data[:200])
print(result)

# Chercher "csaw{" ou "{"
for i, b in enumerate(bytes_data):
    if b == ord('{'):
        print(f"\nTrouvé '{{' à l'index {i}")
        print("Contexte:", ''.join(chr(bytes_data[j]) if 32 <= bytes_data[j] < 127 else '.' for j in range(max(0, i-5), min(len(bytes_data), i+20))))