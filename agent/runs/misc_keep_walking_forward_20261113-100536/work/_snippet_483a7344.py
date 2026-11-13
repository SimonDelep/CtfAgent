import subprocess
import os

# Essayer d'installer p7zip-full
subprocess.run(['apt-get', 'update'], capture_output=True)
subprocess.run(['apt-get', 'install', '-y', 'p7zip-full'], capture_output=True)

# Extraire le 7z
result = subprocess.run(['7z', 'x', 'vcheck.7z', '-o./vcheck_extracted/', '-y'], capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("returncode:", result.returncode)