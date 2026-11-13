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

# Le canal droit a des valeurs entre -16412 et 16388
# Peut-être que les valeurs sont encodées en ASCII décalé?
# Ou peut-être que c'est le canal gauche qui contient le message

# Regardons les valeurs du canal gauche - elles vont de -32768 à 32767
# Peut-être que certaines valeurs spécifiques (comme 0 ou des pics) contiennent l'info

# Trouvons les positions où le canal droit est exactement 0
zero_positions = [i for i, v in enumerate(right_samples) if v == 0]
print(f"Number of zero samples in right channel: {len(zero_positions)}")
print(f"First 20 zero positions: {zero_positions[:20]}")

# Trouvons les positions où le canal droit est non-zero
nonzero_positions = [i for i, v in enumerate(right_samples) if v != 0]
print(f"Number of non-zero samples in right channel: {len(nonzero_positions)}")

# Peut-être que le message est dans les valeurs absolues du canal droit
# Convertissons-les en ASCII si elles sont dans la plage imprimable
ascii_chars = []
for v in right_samples:
    av = abs(v)
    if 32 <= av <= 126:
        ascii_chars.append(chr(av))
    else:
        ascii_chars.append('?')

print("First 200 chars from abs(right):")
print(''.join(ascii_chars[:200]))

# Essayons aussi avec le canal gauche
ascii_chars_left = []
for v in left_samples:
    av = abs(v)
    if 32 <= av <= 126:
        ascii_chars_left.append(chr(av))
    else:
        ascii_chars_left.append('?')

print("\nFirst 200 chars from abs(left):")
print(''.join(ascii_chars_left[:200]))