import subprocess
result = subprocess.run(["python3", "solve.py"], capture_output=True, text=True, timeout=60)
print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print("\nReturn code:", result.returncode)