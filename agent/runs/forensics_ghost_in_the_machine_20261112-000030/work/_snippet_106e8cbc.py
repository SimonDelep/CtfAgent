import subprocess
result = subprocess.run(['python3', '-c', 'from scapy.all import *; print("scapy ok")'], capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)