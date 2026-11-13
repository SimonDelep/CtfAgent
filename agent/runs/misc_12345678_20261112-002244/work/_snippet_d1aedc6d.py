import wave
import struct

# Lire le fichier WAV
w = wave.open('audio.wav', 'rb')
frames = w.readframes(w.getnframes())
w.close()

# Convertir en samples (stéréo: left, right, left, right, ...)
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Séparer les canaux
left_channel = samples[0::2]
right_channel = samples[1::2]

print(f"Samples gauche: {len(left_channel)}, droit: {len(right_channel)}")

# Essayer LSB sur chaque canal séparément
def extract_lsb_text(samples, start=0, length=200):
    lsb_bits = [s & 1 for s in samples[start:start+length*8]]
    bytes_from_lsb = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)
        bytes_from_lsb.append(byte_val)
    return bytes_from_lsb

left_bytes = extract_lsb_text(left_channel)
right_bytes = extract_lsb_text(right_channel)

print("LSB canal gauche (premiers 100 bytes):")
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in left_bytes[:100]))

print("\nLSB canal droit (premiers 100 bytes):")
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in right_bytes[:100]))