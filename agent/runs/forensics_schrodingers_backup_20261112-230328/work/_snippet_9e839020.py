import os
import glob

# Vérifier le workdir actuel
print("CWD:", os.getcwd())
print("Fichiers dans CWD:", os.listdir('.'))

# Chercher catalog.db-wal partout
for root, dirs, files in os.walk('.'):
    for f in files:
        if 'wal' in f.lower():
            print(f"Trouvé: {os.path.join(root, f)}")