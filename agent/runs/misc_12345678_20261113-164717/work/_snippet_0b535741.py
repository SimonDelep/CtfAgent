import subprocess
import re

# Extraire toutes les strings du fichier WAV
result = subprocess.run(['strings', '/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/misc/12345678/12345678 (1).wav'], capture_output=True, text=True)
lines = result.stdout.split('\n')

# Chercher des patterns qui pourraient être un flag ou des parties de flag
patterns = []
for line in lines:
    line = line.strip()
    if len(line) > 3:
        # Chercher des patterns type csaw{...}
        if 'csaw' in line.lower():
            patterns.append(f"csaw trouvé: {line}")
        # Chercher des patterns avec des accolades
        if '{' in line or '}' in line:
            patterns.append(f"Accolades: {line}")
        # Chercher des séquences alphanumériques intéressantes
        if re.match(r'^[A-Za-z0-9_{}@#\$%\^&\*\(\)\-\+=\[\]]{5,}$', line):
            if not any(c.isalpha() for c in line) or any(c.isalpha() for c in line):
                pass  # Trop de bruit

# Afficher les strings les plus longues (potentiellement significatives)
long_strings = [l for l in lines if len(l) >= 10]
print("Strings longues:")
for s in long_strings[:30]:
    print(f"  {s}")

print("\n--- Recherche de 'csaw' ---")
for line in lines:
    if 'csaw' in line.lower():
        print(line)