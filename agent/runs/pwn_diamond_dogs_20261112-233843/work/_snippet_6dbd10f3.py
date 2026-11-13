import subprocess
# Try to use ropper or capstone to disassemble
try:
    result = subprocess.run(['ropper', '--file', 'guard-dog', '--disasm', '--all'], capture_output=True, text=True, timeout=30)
    print(result.stdout[:3000])
    print("STDERR:", result.stderr[:500])
except Exception as e:
    print("ropper error:", e)