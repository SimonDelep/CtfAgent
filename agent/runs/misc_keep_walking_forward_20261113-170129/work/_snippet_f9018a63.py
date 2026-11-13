import sys
sys.path.insert(0, '/tmp/py7zr_pkg')
import py7zr
import os

# Tente d'extraire vcheck.7z
try:
    with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
        print(f"Archives membres:")
        for member in archive.getnames():
            print(f"  {member}")
        archive.extractall(path='vcheck_extracted')
    print("\nExtraction réussie!")
except Exception as e:
    print(f"Erreur: {e}")