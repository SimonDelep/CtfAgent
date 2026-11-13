# Essayons d'utiliser LLL directement avec fpylll ou sage
# D'abord, vérifions ce qui est disponible

try:
    from fpylll import IntegerMatrix, LLL
    print("fpylll disponible")
except ImportError:
    print("fpylll non disponible")

try:
    import sageall
    print("sage disponible")
except ImportError:
    print("sage non disponible")

# Essayons avec numpy pour une réduction de réseau basique
try:
    import numpy as np
    print("numpy disponible")
except ImportError:
    print("numpy non disponible")