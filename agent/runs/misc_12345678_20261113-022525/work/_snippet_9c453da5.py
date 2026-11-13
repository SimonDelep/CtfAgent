# Charger la séquence extraite précédemment et tester différents mappings
import struct
import wave

# Recharger le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    n_channels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    framerate = wav.getframerate()
    n_frames = wav.getnframes()
    raw_data = wav.readframes(n_frames)

# Convertir en samples (16-bit signed)
samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]
print(f"Longueur de la séquence: {len(positive_sequence)}")
print(f"Premiers 100 éléments: {positive_sequence[:100]}")

# Essayer mapping 1=A, 2=B, etc.
decoded = ''.join(chr(ord('A') + v - 1) for v in positive_sequence[:200])
print(f"Mapping 1=A: {decoded}")

# Essayer comme octal (base 8)
# Regrouper par 2 ou 3 et convertir
octal_str = ''.join(str(v) for v in positive_sequence[:50])
print(f"String octale (50 premiers): {octal_str}")

# Essayer de convertir par groupes de 2 (base 8)
for i in range(0, min(100, len(positive_sequence)), 2):
    octal_val = int(str(positive_sequence[i]) + str(positive_sequence[i+1]), 8)
    if 32 <= octal_val < 127:
        print(f"Group {i//2}: {positive_sequence[i]}{positive_sequence[i+1]} -> {octal_val} -> {chr(octal_val)}")