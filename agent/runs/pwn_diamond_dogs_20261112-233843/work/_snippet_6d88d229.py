import subprocess
# Try to use capstone
try:
    result = subprocess.run(['python3', '-c', 'from capstone import *; md = Cs(CS_ARCH_X86, CS_MODE_64); data = open("guard-dog", "rb").read(); print("File size:", len(data))'], capture_output=True, text=True, timeout=30)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr[:1000])
except Exception as e:
    print("Error:", e)