import subprocess
import sys

# Try to disassemble with radare2 or r2pipe
try:
    result = subprocess.run(['r2', '-c', 'pd 200 @ main', '-q', 'thermite-charge'], capture_output=True, text=True, timeout=10)
    print("radare2 output:")
    print(result.stdout)
    print(result.stderr)
except Exception as e:
    print(f"radare2 error: {e}")

# Try with objdump using correct arch
try:
    result = subprocess.run(['objdump', '-D', '-M', 'intel', '-b', 'binary', '-m', 'i386:x86-64', '--start-address=0x1180', '--stop-address=0x1800', 'thermite-charge'], capture_output=True, text=True, timeout=10)
    print("\nobjdump output:")
    print(result.stdout[:2000])
except Exception as e:
    print(f"objdump error: {e}")