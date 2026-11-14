import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles
# Pattern pour Base64 : [A-Za-z0-9+/]{4,}={0,2}
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
b64_strings = b64_pattern.findall(data.decode('latin-1'))  # latin-1 pour éviter les erreurs de décodage

print(f"Nombre de chaînes Base64 trouvées: {len(b64_strings)}")
for i, s in enumerate(b64_strings[:10]):
    print(f"{i}: {s}")
if len(b64_strings) > 10:
    print(f"... et {len(b64_strings)-10} autres")