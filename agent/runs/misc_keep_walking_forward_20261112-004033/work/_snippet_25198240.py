import py7zr
import os

# Extraire le fichier 7z
with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
    archive.extractall(path='extracted')
    
print("Extraction réussie !")
print("Fichiers extraits :")
for root, dirs, files in os.walk('extracted'):
    for f in files:
        filepath = os.path.join(root, f)
        print(f"  {filepath}")
        # Afficher le contenu des fichiers texte
        if f.endswith('.exe') or f.endswith('.dll'):
            print(f"    -> Fichier binaire")
        else:
            try:
                with open(filepath, 'r') as file:
                    content = file.read()
                    print(f"    -> Contenu: {content[:200]}")
            except:
                print(f"    -> Fichier binaire ou encodage spécial")