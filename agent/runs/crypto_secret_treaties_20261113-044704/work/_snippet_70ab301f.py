# Vérifions les bibliothèques disponibles
import sys
print("Python version:", sys.version)

# Essayons d'importer fpylll (LLL en C)
try:
    from fpylll import IntegerMatrix, LLL
    print("fpylll disponible!")
except ImportError:
    print("fpylll non disponible")

# Essayons gmpy2
try:
    import gmpy2
    print("gmpy2 disponible!")
except ImportError:
    print("gmpy2 non disponible")

# Essayons sage via subprocess
import subprocess
result = subprocess.run(['sage', '-c', 'print("sage ok")'], capture_output=True, text=True, timeout=5)
print(f"Sage: {result.stdout.strip() if result.returncode == 0 else 'non disponible'}")