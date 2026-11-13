import subprocess
import sys

# Essayons d'installer scapy dans /tmp/scapy_pkg
result = subprocess.run([sys.executable, "-m", "pip", "install", "scapy", "--target", "/tmp/scapy_pkg"], 
                       capture_output=True, text=True)
print("stdout:", result.stdout[:500] if result.stdout else "none")
print("stderr:", result.stderr[:500] if result.stderr else "none")
print("returncode:", result.returncode)