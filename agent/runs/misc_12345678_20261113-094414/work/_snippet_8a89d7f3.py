import struct

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

# Cherchons les séquences continues de caractères ASCII valides
text = ""
for v in left_channel:
    if 32 <= v <= 126:
        text += chr(v)
    else:
        text += ' '  # Espace pour séparer les mots

# Trouver les plus longues séquences de caractères non-espaces
import re
sequences = re.findall(r'[^\s]{5,}', text)
print(f"Nombre de séquences trouvées: {len(sequences)}")
print("\nPlus longues séquences:")
sequences_sorted = sorted(sequences, key=len, reverse=True)
for seq in sequences_sorted[:20]:
    print(f"  Longueur {len(seq)}: {seq}")