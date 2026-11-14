import subprocess
result = subprocess.run(['apt-get', 'update'], capture_output=True, text=True)
print("apt update:", result.returncode)
result = subprocess.run(['apt-get', 'install', '-y', 'p7zip-full'], capture_output=True, text=True)
print("apt install 7z:", result.returncode)