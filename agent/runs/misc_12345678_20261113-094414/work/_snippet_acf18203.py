import struct
import re

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

# Construire le texte en gardant seulement les caractères ASCII valides
text = ""
for v in left_channel:
    if 32 <= v <= 126:
        text += chr(v)
    else:
        text += ' '

# Trouver toutes les séquences de caractères
sequences = re.findall(r'[^\s]+', text)

# Regardons les séquences qui contiennent des lettres (A-Z, a-z)
letter_sequences = [s for s in sequences if any(c.isalpha() for c in s)]
print(f"Séquences avec lettres: {len(letter_sequences)}")

# Affichons les plus longues séquences avec lettres
letter_sequences_sorted = sorted(letter_sequences, key=len, reverse=True)
print("\nPlus longues séquences avec lettres:")
for seq in letter_sequences_sorted[:15]:
    print(f"  Longueur {len(seq)}: {seq}")

# Peut-être que le message est une combinaison de ces séquences
# Ou peut-être que c'est un message encodé

# Essayons de voir si on peut trouver "csaw" ou "flag" dans le texte
if "csaw" in text.lower():
    print("\nTrouvé 'csaw' dans le texte!")
    idx = text.lower().find("csaw")
    print(f"Contexte: ...{text[max(0,idx-50):idx+50]}...")