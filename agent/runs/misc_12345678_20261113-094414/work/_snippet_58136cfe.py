from PIL import Image
import struct

# D'abord, regardons l'image redimensionnée
img = Image.open('spectrogram_resized2.png')
img_gray = img.convert('L')
pixels = list(img_gray.getdata())

# Trouvons les valeurs extrêmes
min_p = min(pixels)
max_p = max(pixels)
print(f"Pixels: min={min_p}, max={max_p}")

# Cherchons les valeurs les plus fréquentes
from collections import Counter
counts = Counter(pixels)
print("Top 10 valeurs:")
for val, count in counts.most_common(10):
    print(f"  {val}: {count}")

# Maintenant, analysons le canal gauche plus simplement
with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'data')
chunk_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+chunk_size]

num_frames = len(audio_data) // 4

# Extraire canal gauche
left_channel = []
for i in range(num_frames):
    offset = i * 4
    left = struct.unpack('<h', audio_data[offset:offset+2])[0]
    left_channel.append(left)

print(f"\nCanal gauche: {len(left_channel)} échantillons")
print(f"Min: {min(left_channel)}, Max: {max(left_channel)}")

# Cherchons des séquences de valeurs qui pourraient être du texte
# En essayant différents décalages
for shift in [-100, -50, 0, 50, 100]:
    text = ""
    valid = 0
    for v in left_channel[:1000]:  # Juste les 1000 premiers
        c = v + shift
        if 32 <= c <= 126:
            text += chr(c)
            valid += 1
        else:
            text += '.'
    print(f"Shift {shift}: {text}")