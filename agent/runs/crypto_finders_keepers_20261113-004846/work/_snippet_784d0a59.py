# Lire le fichier et chercher des blocs XMP complets
with open('finderskeepers.mp4', 'rb') as f:
    data = f.read()

# Chercher le début et la fin des blocs XMP
xmp_start = data.find(b'<x:xmpmeta')
xmp_end = data.find(b'</x:xmpmeta>')

if xmp_start != -1 and xmp_end != -1:
    xmp_block = data[xmp_start:xmp_end + len(b'</x:xmpmeta>')]
    print("Bloc XMP trouvé:")
    print(xmp_block.decode('utf-8', errors='replace'))
else:
    print("Pas de bloc XMP complet trouvé")
    # Chercher juste des chaînes intéressantes
    print("\nRecherche de chaînes intéressantes:")
    for i, line in enumerate(data.split(b'\n')):
        if len(line) > 10 and b'{' in line or b'_' in line:
            try:
                s = line.decode('utf-8', errors='ignore')
                if any(c.isalpha() for c in s):
                    print(f"Ligne {i}: {s[:100]}")
            except:
                pass