import subprocess
result = subprocess.run(['pip3', 'list'], capture_output=True, text=True)
print(result.stdout)