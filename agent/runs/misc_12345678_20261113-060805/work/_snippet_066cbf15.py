import wave
import struct
import numpy as np
from PIL import Image

# Ouvrir le fichier wav
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Stéréo, 2 bytes par échantillon
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Séparer les canaux
left = np.array([samples[i] for i in range(0, len(samples), 2)])
right = np.array([samples[i] for i in range(1, len(samples), 2)])

# Essayer de voir si le canal droit contient quelque chose de différent
print("Statistiques canal gauche:")
print(f"  Min: {left.min()}, Max: {left.max()}")
print(f"  Moyenne: {left.mean():.2f}, Écart-type: {left.std():.2f}")

print("\nStatistiques canal droit:")
print(f"  Min: {right.min()}, Max: {right.max()}")
print(f"  Moyenne: {right.mean():.2f}, Écart-type: {right.std():.2f}")

# Différence entre canaux
diff = left - right
print("\nStatistiques différence (gauche - droit):")
print(f"  Min: {diff.min()}, Max: {diff.max()}")
print(f"  Moyenne: {diff.mean():.2f}, Écart-type: {diff.std():.2f}")

# Vérifier si la différence contient un message
diff_samples = diff.astype(np.int16)
# Extraire LSB de la différence
lsb_diff = diff_samples & 1
bytes_diff = []
for i in range(0, len(lsb_diff) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_diff[i + j] << j)
    bytes_diff.append(byte_val)

print("\nLSB de la différence - premiers 200 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_diff[:200])
print(result)

# Chercher "csaw{"
flag_start = b'csaw{'.hex()
print(f"\nRecherche de 'csaw{'...'}'")
for i in range(len(bytes_diff) - 5):
    chunk = bytes_diff[i:i+5]
    if chunk == [ord('c'), ord('s'), ord('a'), ord('w'), ord('{')]:
        print(f"Trouvé 'csaw{{' à l'index {i}")
        print("Contexte:", ''.join(chr(bytes_diff[j]) if 32 <= bytes_diff[j] < 127 else '.' for j in range(i, min(len(bytes_diff), i+50))))