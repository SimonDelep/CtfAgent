# Installation avec --break-system-packages
import subprocess
result = subprocess.run(['pip3', 'install', 'capstone', '--break-system-packages', '-q'], capture_output=True, text=True)
print("Installation capstone:", result.returncode)
if result.returncode != 0:
    print("stderr:", result.stderr)
else:
    print("Succès!")