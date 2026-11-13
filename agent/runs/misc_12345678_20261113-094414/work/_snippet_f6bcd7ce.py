from PIL import Image

# Redimensionner le spectrogramme pour le rendre lisible
img = Image.open('spectrogram.png')
print(f"Taille originale: {img.size}")

# Réduire la largeur pour voir le contenu
new_width = 1000
new_height = int(img.size[1] * new_width / img.size[0])
resized = img.resize((new_width, new_height), Image.LANCZOS)
resized.save('spectrogram_resized.png')
print(f"Nouvelle taille: {resized.size}")

# Afficher les premières lignes de pixels pour voir si on distingue quelque chose
pixels = list(resized.getdata())
print(f"Nombre de pixels: {len(pixels)}")