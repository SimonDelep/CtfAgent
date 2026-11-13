# Reprenons l'analyse des métadonnées XMP du MP4
# Vérifions tous les blocs XMP, pas seulement celui avec le Base64

import subprocess
import base64

# Utilisons exiftool ou mp4info pour extraire toutes les métadonnées XMP
result = subprocess.run(['exiftool', '-X', 'finderskeepers.mp4'], capture_output=True, text=True)
print("=== EXIFTOOL XMP OUTPUT ===")
print(result.stdout[:3000])
print("...")
print(result.stdout[-1000:] if len(result.stdout) > 3000 else "")