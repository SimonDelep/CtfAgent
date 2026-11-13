import wave

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

# Peut-être que le message est dans les valeurs du canal droit quand on les interprète comme des caractères
# Les valeurs vont de -16412 à 16388
# Essayons de voir si les valeurs positives forment des caractères ASCII

# Regardons les valeurs uniques qui sont dans la plage ASCII imprimable
ascii_values = set()
for v in right_samples:
    if 32 <= v <= 126:
        ascii_values.add(v)
    elif -126 <= v <= -32:
        ascii_values.add(-v)  # valeurs négatives aussi

print(f"ASCII values found in right channel: {sorted(ascii_values)}")
print(f"Characters: {''.join(chr(v) for v in sorted(ascii_values))}")

# Essayons aussi avec le canal gauche
ascii_values_left = set()
for v in left_samples:
    if 32 <= v <= 126:
        ascii_values_left.add(v)
    elif -126 <= v <= -32:
        ascii_values_left.add(-v)

print(f"\nASCII values found in left channel: {sorted(ascii_values_left)}")
print(f"Characters: {''.join(chr(v) for v in sorted(ascii_values_left))}")

# Peut-être que le message est dans l'ordre d'apparition des valeurs ASCII
# Extraire les valeurs ASCII dans l'ordre
ascii_sequence_right = []
for v in right_samples:
    if 32 <= v <= 126:
        ascii_sequence_right.append(chr(v))
    elif -126 <= v <= -32:
        ascii_sequence_right.append(chr(-v))

print(f"\nASCII sequence from right channel (first 500):")
print(''.join(ascii_sequence_right[:500]))