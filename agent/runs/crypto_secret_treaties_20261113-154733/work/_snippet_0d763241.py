import sys
print("Python version:", sys.version)
try:
    import numpy as np
    print("numpy disponible")
except:
    print("numpy manquant")
try:
    from fpylll import IntegerMatrix, LLL
    print("fpylll disponible")
except Exception as e:
    print("fpylll:", e)