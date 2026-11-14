import base64
import re

# Re-lisons le fichier WAV pour extraire les chaînes Base64
with open('12345678 (1).wav', 'rb') as f:
    data = f.read()

# Extraction regex des chaînes Base64
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
matches = b64_pattern.findall(data.decode('latin-1'))  # latin-1 pour éviter les erreurs de décodage

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")
for i, m in enumerate(matches):
    print(f"{i}: {m}")