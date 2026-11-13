# Essayons d'implémenter LLL en Python pur
# Ou utilisons une approche de recherche de trapdoor

# D'abord, vérifions si on peut utiliser sympy pour les inverses modulaires
try:
    from sympy import mod_inverse
    print("sympy disponible")
except ImportError:
    print("sympy non disponible")

# Vérifions aussi si on a access à sage via subprocess
import subprocess
result = subprocess.run(['which', 'sage'], capture_output=True, text=True)
print(f"sage path: {result.stdout.strip()}")