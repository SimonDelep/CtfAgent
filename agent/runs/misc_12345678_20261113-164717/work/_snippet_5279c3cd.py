import base64
encoded = "Ml81dDNAMV8="
try:
    decoded = base64.b64decode(encoded).decode('utf-8', errors='replace')
    print(f"Base64 décodé: {decoded}")
except Exception as e:
    print(f"Erreur: {e}")

# Essayons aussi de chercher le flag directement dans les strings
import subprocess
result = subprocess.run(['strings', '/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/misc/12345678/12345678 (1).wav'], capture_output=True, text=True)
lines = result.stdout.split('\n')
for line in lines:
    if 'csaw' in line.lower() or 'flag' in line.lower():
        print(f"Potentiel flag: {line}")