try:
    from capstone import *
    print("capstone disponible")
except ImportError:
    print("capstone manquant")