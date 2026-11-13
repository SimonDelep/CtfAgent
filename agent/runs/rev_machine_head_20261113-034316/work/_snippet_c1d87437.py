# Installation de capstone
import subprocess
result = subprocess.run(['pip3', 'install', 'capstone', '-q'], capture_output=True, text=True)
print("Installation capstone:", result.returncode)
if result.returncode != 0:
    print("stderr:", result.stderr)