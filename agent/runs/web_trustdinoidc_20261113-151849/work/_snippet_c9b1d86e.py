import subprocess
result = subprocess.run(["python3", "solve.py"], capture_output=True, text=True, timeout=30)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)