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

# Cherchons "csaw" ou "flag" avec différents décalages
def caesar_decrypt(text, shift):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base - shift) % 26 + base)
        else:
            result += c
    return result

# Cherchons dans le texte original d'abord
print("Recherche dans le texte original:")
if "csaw" in text.lower():
    print("  Trouvé 'csaw'!")
if "flag" in text.lower():
    print("  Trouvé 'flag'!")

# Essayons de trouver des mots anglais courants
common_words = ["the", "and", "for", "are", "but", "not", "you", "all", "can", "had"]
for word in common_words:
    if word in text.lower():
        print(f"  Trouvé '{word}'!")

# Peut-être que le message est dans le canal droit aussi
with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'data')
chunk_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+chunk_size]

num_frames = len(audio_data) // 4

# Extraire canal droit
right_channel = []
for i in range(num_frames):
    offset = i * 4
    right = struct.unpack('<h', audio_data[offset+2:offset+4])[0]
    right_channel.append(right)

# Construire le texte du canal droit
text_right = ""
for v in right_channel:
    if 32 <= v <= 126:
        text_right += chr(v)
    else:
        text_right += ' '

print("\nCanal droit - recherche de 'csaw' ou 'flag':")
if "csaw" in text_right.lower():
    print("  Trouvé 'csaw'!")
if "flag" in text_right.lower():
    print("  Trouvé 'flag'!")

# Affichons quelques séquences du canal droit
sequences_right = re.findall(r'[^\s]+', text_right)
sequences_right_sorted = sorted(sequences_right, key=len, reverse=True)
print("\nPlus longues séquences du canal droit:")
for seq in sequences_right_sorted[:5]:
    print(f"  Longueur {len(seq)}: {seq[:100]}")