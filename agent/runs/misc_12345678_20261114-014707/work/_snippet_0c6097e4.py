import base64
import re

with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraction regex des chaînes Base64
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
matches = b64_pattern.findall(data.decode('latin-1'))

print("Toutes les chaînes Base64:")
for i, m in enumerate(matches):
    print(f"{i}: {m}")

# Peut-être que certaines chaînes sont en fait du texte ASCII qui ressemble à du Base64
# Mais qui est en fait le flag directement?
print("\n---")
print("Cherchons des patterns qui ressemblent à 'csaw' ou 'flag':")
for i, m in enumerate(matches):
    if 'csaw' in m.lower() or 'flag' in m.lower() or 'csw' in m.lower():
        print(f"Match potentiel: {i}: {m}")