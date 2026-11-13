import subprocess
result = subprocess.run(['python3', '-c', 'import py7zr; import sys; print("py7zr available")'], capture_output=True, text=True)
print(result.stdout, result.stderr)