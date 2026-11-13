import subprocess
import base64
import re

# D'abord, vérifions si ffmpeg est disponible
result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
print(f"ffmpeg: {result.stdout.strip()}")

# Extraire les chaînes du fichier MP4
result = subprocess.run(['strings', 'finderskeepers.mp4'], capture_output=True, text=True)
strings = result.stdout.split('\n')

# Chercher le Base64 et autres chaînes intéressantes
print("\n=== Chaînes potentiellement intéressantes ===")
for s in strings:
    if len(s) > 10:
        # Chercher des patterns de Base64
        if re.match(r'^[A-Za-z0-9+/=]{20,}$', s):
            print(f"Base64: {s}")
            try:
                decoded = base64.b64decode(s).decode('utf-8', errors='ignore')
                print(f"  -> Décodé: {decoded}")
            except:
                pass

# Chercher aussi des chaînes avec des accolades
print("\n=== Chaînes avec accolades ===")
for s in strings:
    if '{' in s and '}' in s:
        print(f"  {s}")

# Chercher des chaînes qui pourraient être des mots
print("\n=== Autres chaînes longues ===")
for s in strings:
    if len(s) > 15 and len(s) < 100:
        # Vérifier si c'est du texte lisible
        if re.match(r'^[a-zA-Z0-9_{}@]+$', s):
            print(f"  {s}")
