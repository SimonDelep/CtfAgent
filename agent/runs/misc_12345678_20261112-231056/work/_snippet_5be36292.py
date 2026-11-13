import wave

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Le WAV est stéréo, 16-bit. Chaque échantillon est 2 bytes.
# Interprétons comme des échantillons signed 16-bit little-endian
import struct

# Décoder tous les échantillons
samples = []
for i in range(0, len(data), 2):
    if i + 1 < len(data):
        sample = struct.unpack('<h', data[i:i+2])[0]
        samples.append(sample)

print(f"Nombre d'échantillons: {len(samples)}")
print("Premiers 50 échantillons:", samples[:50])

# Séparer canaux gauche et droit (stéréo = L, R, L, R, ...)
left = samples[0::2]
right = samples[1::2]

print(f"\nCanal gauche (premiers 20): {left[:20]}")
print(f"Canal droit (premiers 20): {right[:20]}")

# Essayer le XOR des canaux
xor_samples = [l ^ r for l, r in zip(left, right)]
print(f"\nXOR L^R (premiers 50): {xor_samples[:50]}")

# Essayer la différence
diff_samples = [l - r for l, r in zip(left, right)]
print(f"\nDifférence L-R (premiers 50): {diff_samples[:50]}")