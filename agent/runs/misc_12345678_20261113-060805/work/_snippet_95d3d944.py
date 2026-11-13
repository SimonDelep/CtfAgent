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

# Peut-être que le message est dans le canal droit seul avec un décalage
# Ou peut-être qu'il faut regarder les bits de manière différente

# Essayer d'extraire les bits de poids faible du canal droit uniquement
lsb_right = [r & 1 for r in right]
bytes_right = []
for i in range(0, len(lsb_right) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_right[i + j] << j)
    bytes_right.append(byte_val)

print("LSB canal droit - premiers 300 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_right[:300])
print(result)

# Chercher "csaw{"
print("\nRecherche de 'csaw{' dans canal droit LSB...")
for i in range(len(bytes_right) - 5):
    chunk = bytes_right[i:i+5]
    if chunk == [ord('c'), ord('s'), ord('a'), ord('w'), ord('{')]:
        print(f"Trouvé 'csaw{{' à l'index {i}")
        context = ''.join(chr(bytes_right[j]) if 32 <= bytes_right[j] < 127 else '.' for j in range(i, min(len(bytes_right), i+60)))
        print("Contexte:", context)