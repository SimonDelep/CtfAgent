import subprocess
import sys

# Vérifier si capstone est installé
result = subprocess.run([sys.executable, "-c", "import capstone; print(capstone.__version__)"], capture_output=True, text=True)
print("capstone version:", result.stdout.strip() if result.returncode == 0 else "NOT FOUND")
print("stderr:", result.stderr.strip())