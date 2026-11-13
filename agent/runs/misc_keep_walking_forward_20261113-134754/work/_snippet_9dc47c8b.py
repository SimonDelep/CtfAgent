import py7zr
import os

# Liste des fichiers
print("Fichiers dans le workdir:")
for f in os.listdir('.'):
    print(f"  {f}")

# Extraction de l'archive 7z
print("\nExtraction de vcheck.7z...")
with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
    archive.extractall(path='.')
print("Extraction terminée!")

# Liste des fichiers extraits
print("\nFichiers extraits:")
for root, dirs, files in os.walk('.'):
    for f in files:
        path = os.path.join(root, f)
        if not path.endswith('.7z'):
            print(f"  {path}")