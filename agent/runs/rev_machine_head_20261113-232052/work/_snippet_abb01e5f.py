import subprocess
import sys

# D'abord, vérifions si capstone est installé
result = subprocess.run([sys.executable, "-c", "import capstone; print('capstone OK')"], capture_output=True, text=True)
print("Capstone check:", result.stdout.strip(), result.stderr.strip())

# Essayons avec objdump pour voir le code
result = subprocess.run(["objdump", "-d", "-M", "intel", "masterkey"], capture_output=True, text=True)
lines = result.stdout.split('\n')
# Cherchons les fonctions intéressantes
for i, line in enumerate(lines[:200]):
    print(line)