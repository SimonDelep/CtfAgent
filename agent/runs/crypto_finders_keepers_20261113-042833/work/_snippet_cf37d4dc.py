import subprocess
result = subprocess.run(['pip3', 'show', 'av'], capture_output=True, text=True)
print("av:", result.stdout if result.stdout else "non installé")
result = subprocess.run(['pip3', 'show', 'imageio'], capture_output=True, text=True)
print("imageio:", result.stdout if result.stdout else "non installé")