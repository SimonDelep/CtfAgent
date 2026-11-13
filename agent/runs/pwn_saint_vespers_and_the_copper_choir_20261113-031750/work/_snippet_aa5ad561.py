import os
import sys

# Liste tous les fichiers avec leurs tailles
files = []
for f in os.listdir('.'):
    try:
        size = os.path.getsize(f)
        files.append((f, size))
    except:
        pass

# Trier par taille
files.sort(key=lambda x: x[1], reverse=True)

for name, size in files[:15]:
    print(f"{size:8d} bytes: {repr(name)}")