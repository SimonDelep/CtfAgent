# Vérifions les modules disponibles
import sys
print("Modules disponibles:")
try:
    import fpylll
    print("fpylll disponible")
except:
    print("fpylll non disponible")

try:
    from fpylll import IntegerMatrix, LLL
    print("fpylll LLL importable")
except Exception as e:
    print(f"fpylll LLL erreur: {e}")

try:
    import numpy as np
    print("numpy disponible")
except:
    print("numpy non disponible")