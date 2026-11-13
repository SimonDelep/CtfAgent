import subprocess
import os

# Essayer de lancer avec qemu-x86-64
try:
    result = subprocess.run(['qemu-x86-64', '-L', '/usr/x86_64-linux-gnu', './vespers'], 
                          input=b'9\n', capture_output=True, timeout=5)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    print("returncode:", result.returncode)
except FileNotFoundError as e:
    print("QEMU not found:", e)
except Exception as e:
    print("Error:", e)