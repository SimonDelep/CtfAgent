# Essayer d'importer capstone
try:
    from capstone import *
    print("capstone disponible")
except ImportError:
    print("capstone non disponible, essayons zydis ou désassembleur manuel")
