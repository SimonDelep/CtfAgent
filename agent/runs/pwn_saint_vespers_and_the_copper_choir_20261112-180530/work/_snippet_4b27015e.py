import subprocess
import os

# Vérifier les fichiers copiés
print("Fichiers dans le workdir:")
for f in os.listdir("."):
    try:
        print(f"  {f}")
    except:
        print(f"  {repr(f)}")

# Analyse du binaire avec readelf
print("\n=== readelf -h vespers ===")
result = subprocess.run(["readelf", "-h", "vespers"], capture_output=True, text=True, errors='replace')
print(result.stdout[:2000])

print("\n=== readelf -s vespers (symboles) ===")
result = subprocess.run(["readelf", "-s", "vespers"], capture_output=True, text=True, errors='replace')
print(result.stdout[:3000])