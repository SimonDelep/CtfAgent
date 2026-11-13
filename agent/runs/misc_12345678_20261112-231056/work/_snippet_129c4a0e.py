import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Décoder comme signed 16-bit
samples = []
for i in range(0, len(data), 2):
    if i + 1 < len(data):
        sample = struct.unpack('<h', data[i:i+2])[0]
        samples.append(sample)

# Essayer différents plans de bits
for bit in range(8):
    bits = [(abs(s) >> bit) & 1 for s in samples]
    # Convertir en bytes
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (bits[i + j] << (7 - j))
        result.append(byte_val)
    
    # Afficher les premiers caractères imprimables
    text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in result[:100])
    print(f"Bit {bit}: {text}")