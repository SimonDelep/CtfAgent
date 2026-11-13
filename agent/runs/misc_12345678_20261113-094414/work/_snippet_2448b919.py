from PIL import Image

# Regardons l'image redimensionnée
img = Image.open('spectrogram_resized2.png')
print(f"Taille: {img.size}")

# Convertissons en niveaux de gris et cherchons des motifs
img_gray = img.convert('L')
pixels = list(img_gray.getdata())

# Trouvons les valeurs de pixels
min_p = min(pixels)
max_p = max(pixels)
print(f"Valeurs de pixels: min={min_p}, max={max_p}")

# Cherchons des zones avec des valeurs spécifiques (peut-être du texte en noir sur fond blanc ou inversement)
# Si c'est un spectrogramme, le texte pourrait être en contraste élevé

# Comptons les occurrences de chaque valeur
from collections import Counter
counts = Counter(pixels)
print("Top 20 valeurs de pixels:")
for val, count in counts.most_common(20):
    print(f"  {val}: {count}")

# Essayons de voir si on peut extraire du texte en regardant les transitions
# Ou peut-être que le message est écrit dans le spectre de fréquence

# Regardons aussi le canal gauche
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

# Le canal gauche avait des fragments lisibles - regardons de plus près
# Peut-être que certaines valeurs correspondent à des caractères ASCII décalés
print("\nAnalyse canal gauche:")
print(f"Min: {min(left_channel)}, Max: {max(left_channel)}")

# Essayons de trouver des plages où les valeurs sont dans une plage étroite qui pourrait correspondre à du texte
# Si on décale les valeurs pour les mettre dans la plage ASCII
for shift in range(-200, 200, 50):
    text = ""
    valid_count = 0
    for v in left_channel:
        c = v + shift
        if 32 <= c <= 126:
            text += chr(c)
            valid_count += 1
        else:
            text += '?'
    
    # Vérifions s'il y a beaucoup de caractères valides
    if valid_count > len(left_channel) * 0.5:
        print(f"Shift {shift}: valid={valid_count}/{len(left_channel)}")
        # Afficher un échantillon
        print(f"  Exemple: {text[:200]}")