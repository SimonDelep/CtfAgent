import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Séparer les canaux
left = samples[0::2]
right = samples[1::2]

# Essayer LSB sur chaque canal séparément
def extract_lsb_bytes(samples):
    lsb_bits = [s & 1 for s in samples]
    lsb_bytes = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)
        lsb_bytes.append(byte_val)
    return lsb_bytes

left_bytes = extract_lsb_bytes(left)
right_bytes = extract_lsb_bytes(right)

print("LSB Left (first 100):", bytes(left_bytes[:100]))
print("LSB Left printable:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in left_bytes[:200]))
print()
print("LSB Right (first 100):", bytes(right_bytes[:100]))
print("LSB Right printable:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in right_bytes[:200]))
