import wave
import struct

# Ouvrir le fichier wav
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Stéréo, 2 bytes par échantillon
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Séparer les canaux
left = [samples[i] for i in range(0, len(samples), 2)]
right = [samples[i] for i in range(1, len(samples), 2)]

# Statistiques
print("Statistiques canal gauche:")
print(f"  Min: {min(left)}, Max: {max(left)}")
print(f"  Moyenne: {sum(left)/len(left):.2f}")

print("\nStatistiques canal droit:")
print(f"  Min: {min(right)}, Max: {max(right)}")
print(f"  Moyenne: {sum(right)/len(right):.2f}")

# Différence entre canaux
diff = [left[i] - right[i] for i in range(len(left))]
print("\nStatistiques différence (gauche - droit):")
print(f"  Min: {min(diff)}, Max: {max(diff)}")
print(f"  Moyenne: {sum(diff)/len(diff):.2f}")

# Extraire LSB de la différence
lsb_diff = [d & 1 for d in diff]
bytes_diff = []
for i in range(0, len(lsb_diff) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_diff[i + j] << j)
    bytes_diff.append(byte_val)

print("\nLSB de la différence - premiers 300 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_diff[:300])
print(result)

# Chercher "csaw{"
print("\nRecherche de 'csaw{'...")
for i in range(len(bytes_diff) - 5):
    chunk = bytes_diff[i:i+5]
    if chunk == [ord('c'), ord('s'), ord('a'), ord('w'), ord('{')]:
        print(f"Trouvé 'csaw{{' à l'index {i}")
        context = ''.join(chr(bytes_diff[j]) if 32 <= bytes_diff[j] < 127 else '.' for j in range(i, min(len(bytes_diff), i+60)))
        print("Contexte:", context)