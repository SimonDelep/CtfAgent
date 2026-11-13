from PIL import Image

img = Image.open('spectrogram.png')
w, h = img.size
print(f"Taille originale: {w}x{h}")

# Le spectrogramme est très large. Peut-être que le message est écrit en travers.
# Essayons de créer une version où on réduit la largeur mais on garde plus de hauteur
# Ou on pourrait essayer de voir si le message est dans les basses fréquences (en haut ou en bas de l'image)

# D'abord, regardons la distribution des couleurs dans l'image
img_rgb = img.convert('RGB')
pixels = list(img_rgb.getdata())

# Comptons les couleurs
from collections import Counter
# Arrondissons les couleurs pour regrouper les similaires
def round_color(c, step=32):
    return (c[0]//step*step, c[1]//step*step, c[2]//step*step)

rounded = [round_color(p) for p in pixels]
counts = Counter(rounded)
print("Top 10 couleurs (arrondies):")
for color, count in counts.most_common(10):
    print(f"  {color}: {count}")

# Le fond est probablement une couleur dominante, et le texte une autre
# Cherchons les couleurs qui apparaissent le moins (peut-être le texte)
print("\nCouleurs les plus rares (non-noir):")
for color, count in counts.most_common()[:-11:-1]:  # Les 10 dernières
    if color != (0, 0, 0):
        print(f"  {color}: {count}")