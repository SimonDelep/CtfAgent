import subprocess
# Essayons avec readelf -s pour voir les symboles
result = subprocess.run(['readelf', '-s', 'thermite-charge'], capture_output=True, text=True, timeout=15)
print("Symboles:")
print(result.stdout)