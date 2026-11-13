import sys
sys.path.insert(0, '/tmp/py7zr_pkg')
import py7zr
import os

# Liste les fichiers dans le workdir
print("Fichiers dans le workdir:")
for f in os.listdir('.'):
    print(f"  {f}")

# Tente d'extraire vcheck.7z
try:
    with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
        print(f"\nContenu de l'archive:")
        archive.listall()
        archive.extractall(path='vcheck_extracted')
    print("\nExtraction réussie!")
except Exception as e:
    print(f"Erreur: {e}")