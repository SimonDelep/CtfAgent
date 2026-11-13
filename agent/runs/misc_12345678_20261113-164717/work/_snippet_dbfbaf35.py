import base64
import re

# Chemin du fichier WAV
wav_path = "/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/csaw/CSAW-Quals/misc/12345678/12345678 (1).wav"

# Lire le fichier en binaire
with open(wav_path, 'rb') as f:
    data = f.read()

# Chercher toutes les chaînes Base64 potentielles (min 4 chars, max 100)
base64_pattern = rb'[A-Za-z0-9+/]{4,100}={0,2}'
matches = re.findall(base64_pattern, data)

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")
for i, m in enumerate(matches):
    try:
        decoded = base64.b64decode(m).decode('utf-8', errors='replace')
        print(f"{i}: {m.decode('utf-8', errors='replace')} -> {decoded}")
    except:
        print(f"{i}: {m.decode('utf-8', errors='replace')} -> (échec décodage)")