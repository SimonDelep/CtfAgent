import subprocess
# Try to use pwn tools to disassemble
try:
    result = subprocess.run(['python3', '-c', 'from pwn import *; print(disasm(raw(open("guard-dog", "rb").read())))'], capture_output=True, text=True, timeout=60)
    print("STDOUT:", result.stdout[:5000])
    print("STDERR:", result.stderr[:1000])
except Exception as e:
    print("Error:", e)