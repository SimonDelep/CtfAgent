import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

print(f"Total samples: {len(samples)}")

# Séparer les canaux
left = samples[0::2]
right = samples[1::2]

print(f"Left samples: {len(left)}, Right samples: {len(right)}")

# Vérifier la différence entre canaux
diff = [abs(l - r) for l, r in zip(left, right)]
print(f"Difference samples: {len(diff)}")

# Regarder les valeurs de différence
print(f"Min diff: {min(diff)}, Max diff: {max(diff)}")

# Extraire LSB de la différence
diff_lsb = [d & 1 for d in diff]
diff_bytes = []
for i in range(0, len(diff_lsb) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (diff_lsb[i + j] << j)
    diff_bytes.append(byte_val)

print(f"Diff LSB bytes (first 100): {bytes(diff_bytes[:100])}")
print(f"Diff LSB printable: {''.join(chr(b) if 32 <= b < 127 else '.' for b in diff_bytes[:200])}")
