import wave
import math
from PIL import Image

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())

# Extraire les canaux
left_samples = []
right_samples = []

for i in range(0, len(data), 4):
    if i + 3 < len(data):
        left_val = int.from_bytes(data[i:i+2], 'little', signed=True)
        right_val = int.from_bytes(data[i+2:i+4], 'little', signed=True)
        left_samples.append(left_val)
        right_samples.append(right_val)

# Utiliser le canal droit (le plus silencieux, peut-être caché)
samples = right_samples

# FFT simple pour spectrogramme
# On va diviser en fenêtres et calculer la puissance pour chaque fréquence

def fft_simple(signal):
    """FFT naive pour petite taille"""
    n = len(signal)
    if n <= 1:
        return signal
    # FFT radix-2
    if n & (n-1) != 0:
        # Pad to next power of 2
        new_n = 1
        while new_n < n:
            new_n *= 2
        signal = list(signal) + [0] * (new_n - n)
        n = new_n
    
    # Cooley-Tukey
    result = list(signal)
    bits = n.bit_length() - 1
    
    # Bit-reversal permutation
    for i in range(n):
        j = int(bin(i)[2:].zfill(bits)[::-1], 2)
        if i < j:
            result[i], result[j] = result[j], result[i]
    
    # FFT
    length = 2
    while length <= n:
        angle = 2 * math.pi / length
        wlen = complex(math.cos(angle), -math.sin(angle))
        for i in range(0, n, length):
            w = complex(1, 0)
            for j in range(length // 2):
                u = result[i + j]
                v = result[i + j + length // 2] * w
                result[i + j] = u + v
                result[i + j + length // 2] = u - v
                w *= wlen
        length *= 2
    
    return result

# Paramètres
frame_size = 256  # taille de fenêtre
hop_size = 128    # chevauchement
num_frames = (len(samples) - frame_size) // hop_size + 1

# Créer une image spectrogramme
width = num_frames
height = frame_size // 2  # seulement les fréquences positives

print(f"Creating spectrogram: {width}x{height}")

# Calculer le spectrogramme
spectrogram = [[0] * width for _ in range(height)]

for frame_idx in range(width):
    start = frame_idx * hop_size
    if start + frame_size > len(samples):
        break
    
    # Extraire la fenêtre
    window = samples[start:start + frame_size]
    
    # Appliquer fenêtre de Hann
    hann = [0.5 * (1 - math.cos(2 * math.pi * i / (frame_size - 1))) for i in range(frame_size)]
    window = [window[i] * hann[i] for i in range(frame_size)]
    
    # FFT
    fft_result = fft_simple(window)
    
    # Calculer la puissance pour chaque fréquence
    for freq_idx in range(height):
        real = fft_result[freq_idx].real
        imag = fft_result[freq_idx].imag
        power = math.sqrt(real * real + imag * imag)
        spectrogram[freq_idx][frame_idx] = power

# Normaliser et convertir en image
max_power = max(max(col) for col in spectrogram) if spectrogram else 1

img = Image.new('RGB', (width, height))
for y in range(height):
    for x in range(width):
        val = int(255 * spectrogram[y][x] / max_power) if max_power > 0 else 0
        # Inverser les couleurs pour que les fortes puissances soient claires
        img.putpixel((x, y), (val, val, val))

img.save('spectrogram.png')
print("Spectrogram saved to spectrogram.png")

# Afficher quelques valeurs pour vérifier
print(f"Sample spectrogram values (first 10x10):")
for y in range(10):
    row = [spectrogram[y][x] for x in range(10)]
    print([f"{v:.1f}" for v in row])