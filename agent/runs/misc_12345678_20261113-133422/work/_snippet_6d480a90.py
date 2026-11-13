import sys
print("Python version:", sys.version)
try:
    import numpy as np
    print("numpy version:", np.__version__)
except ImportError as e:
    print("numpy error:", e)

try:
    import matplotlib
    print("matplotlib version:", matplotlib.__version__)
except ImportError as e:
    print("matplotlib error:", e)