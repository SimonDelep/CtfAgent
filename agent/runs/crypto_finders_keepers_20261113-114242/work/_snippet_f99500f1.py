# Relisons le fichier MP4 pour extraire les métadonnées XMP
import subprocess
result = subprocess.run(['strings', 'finderskeepers.mp4'], capture_output=True, text=True)
lines = result.stdout.split('\n')

# Cherchons la chaîne base64
for line in lines:
    if 'ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=' in line:
        print(f"Trouvé: {line}")
    # Cherchons aussi d'autres chaînes intéressantes
    if 'esnp' in line.lower() or 'csaw' in line.lower():
        print(f"Intéressant: {line}")