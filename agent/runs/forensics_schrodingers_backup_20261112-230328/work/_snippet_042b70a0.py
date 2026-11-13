import os

# Listons tous les fichiers dans le dossier courant
for f in os.listdir('.'):
    print(f"{f}: {os.path.getsize(f)} bytes")