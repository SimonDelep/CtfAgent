import subprocess
import os

# Lister les fichiers extraits
print("Fichiers dans le workdir:")
for f in os.listdir('.'):
    print(f"  {f}")

# Essayer de faire des strings sur vcheck.exe
print("\n--- Strings de vcheck.exe (premières lignes) ---")
result = subprocess.run(['strings', 'vcheck.exe'], capture_output=True, text=True)
lines = result.stdout.split('\n')[:50]
for line in lines:
    print(line)

print("\n--- Strings de version.dll (premières lignes) ---")
result = subprocess.run(['strings', 'version.dll'], capture_output=True, text=True)
lines = result.stdout.split('\n')[:50]
for line in lines:
    print(line)