from PIL import Image

img = Image.open('spectrogram.png')
w, h = img.size

# Convertir en niveaux de gris
img_gray = img.convert('L')

# Créer une nouvelle image où on ne garde que les pixels non-noirs
# et on les met en blanc sur fond noir
new_img = Image.new('L', (w, h), 0)

pixels_src = list(img_gray.getdata())
pixels_dst = list(new_img.getdata())

for i, p in enumerate(pixels_src):
    if p > 0:  # Si le pixel n'est pas noir
        pixels_dst[i] = 255  # Mettre en blanc

new_img.putdata(pixels_dst)

# Maintenant, cherchons des zones avec des pixels blancs qui pourraient former du texte
# Le texte serait probablement des zones continues de pixels blancs

# Convertir en binaire et chercher des motifs
binary_pixels = [1 if p > 0 else 0 for p in pixels_src]

# Regardons la distribution des pixels non-noirs
non_black = sum(1 for p in binary_pixels if p == 1)
print(f"Pixels non-noirs: {non_black} sur {len(binary_pixels)}")
print(f"Pourcentage: {100*non_black/len(binary_pixels):.2f}%")

# Si c'est un spectrogramme normal, les pixels non-noirs devraient former des motifs
# Peut-être que le message est écrit en utilisant les fréquences

# Essayons de voir si on peut extraire du texte en regardant les colonnes
# Chaque colonne représente un instant dans le temps, chaque ligne une fréquence

# Si le message est écrit, il pourrait être visible en regardant les pixels non-noirs
# Créons une image simplifiée pour visualiser
new_img.save('spectrogram_binary.png')
print("Image binaire sauvegardée: spectrogram_binary.png")

# Regardons aussi si on peut trouver des séquences de pixels blancs dans une ligne spécifique
# Peut-être que le message est dans une bande de fréquence spécifique

# Trouvons les lignes (fréquences) qui ont le plus de pixels blancs
line_counts = [0] * h
for y in range(h):
    for x in range(w):
        idx = y * w + x
        if binary_pixels[idx] == 1:
            line_counts[y] += 1

print("\nLignes avec le plus de pixels blancs:")
sorted_lines = sorted(enumerate(line_counts), key=lambda x: x[1], reverse=True)
for line, count in sorted_lines[:10]:
    print(f"  Ligne {line}: {count} pixels")