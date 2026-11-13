import sys
print("Python path:", sys.path)
try:
    import numpy as np
    print("numpy version:", np.__version__)
except Exception as e:
    print("Error importing numpy:", e)