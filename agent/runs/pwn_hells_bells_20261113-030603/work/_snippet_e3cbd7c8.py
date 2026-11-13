import subprocess

# Use readelf to get symbols and functions
result = subprocess.run(['readelf', '-s', 'thermite-charge'], capture_output=True, text=True, timeout=10)
print("Symbols:")
print(result.stdout)