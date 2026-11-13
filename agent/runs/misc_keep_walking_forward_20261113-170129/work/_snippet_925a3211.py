import subprocess
# Essayons d'utiliser python3 -m pip install py7zr dans un venv temporaire
result = subprocess.run(['python3', '-m', 'pip', 'install', 'py7zr', '--target', '/tmp/py7zr_pkg'], capture_output=True, text=True)
print("stdout:", result.stdout[:500] if result.stdout else "none")
print("stderr:", result.stderr[:500] if result.stderr else "none")
print("returncode:", result.returncode)