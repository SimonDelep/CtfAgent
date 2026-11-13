import subprocess
import os

# Installer py7zr pour extraire le 7z
subprocess.run(['pip', 'install', '-q', 'py7zr'], capture_output=True)

import py7zr

# Extraire le 7z
with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
    archive.extractall(path='./vcheck_extracted/')

print("Extraction terminée")
print("Fichiers extraits:")
for root, dirs, files in os.walk('./vcheck_extracted/'):
    for f in files:
        print(os.path.join(root, f))