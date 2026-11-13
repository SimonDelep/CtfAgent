import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Séparer les canaux
left = samples[0::2]
right = samples[1::2]

# Essayer valeurs absolues modulo 128
def mod128_bytes(samples):
    return [abs(s) % 128 for s in samples]

left_mod = mod128_bytes(left)
right_mod = mod128_bytes(right)

print("Left mod 128 (first 100):", bytes(left_mod[:100]))
print("Left mod 128 printable:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in left_mod[:200]))
print()
print("Right mod 128 (first 100):", bytes(right_mod[:100]))
print("Right mod 128 printable:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in right_mod[:200]))
