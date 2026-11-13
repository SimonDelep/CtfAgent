import py7zr
import os

# Vérifier si py7zr fonctionne
try:
    with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
        archive.extractall(path='extracted')
    print("Extraction réussie !")
    print("Fichiers extraits :")
    for root, dirs, files in os.walk('extracted'):
        for f in files:
            print(f"  {os.path.join(root, f)}")
except Exception as e:
    print(f"Erreur : {e}")