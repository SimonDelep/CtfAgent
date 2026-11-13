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

# Peut-être que le message est dans les valeurs brutes des échantillons
# Convertir les échantillons en bytes et chercher des motifs

# Essayer de convertir les échantillons directement en ASCII (en prenant les 8 bits de poids faible)
left_bytes = [l & 0xFF for l in left]
right_bytes = [r & 0xFF for r in right]

print("Canal gauche (8 bits de poids faible) - premiers 200 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in left_bytes[:200])
print(result)

print("\nCanal droit (8 bits de poids faible) - premiers 200 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in right_bytes[:200])
print(result)

# Chercher "csaw{"
print("\nRecherche de 'csaw{' dans canal gauche...")
for i in range(len(left_bytes) - 5):
    chunk = left_bytes[i:i+5]
    if chunk == [ord('c'), ord('s'), ord('a'), ord('w'), ord('{')]:
        print(f"Trouvé 'csaw{{' à l'index {i}")
        context = ''.join(chr(left_bytes[j]) if 32 <= left_bytes[j] < 127 else '.' for j in range(i, min(len(left_bytes), i+60)))
        print("Contexte:", context)

print("\nRecherche de 'csaw{' dans canal droit...")
for i in range(len(right_bytes) - 5):
    chunk = right_bytes[i:i+5]
    if chunk == [ord('c'), ord('s'), ord('a'), ord('w'), ord('{')]:
        print(f"Trouvé 'csaw{{' à l'index {i}")
        context = ''.join(chr(right_bytes[j]) if 32 <= right_bytes[j] < 127 else '.' for j in range(i, min(len(right_bytes), i+60)))
        print("Contexte:", context)