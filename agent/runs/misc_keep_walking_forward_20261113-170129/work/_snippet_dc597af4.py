import sys
sys.path.insert(0, '/tmp/py7zr_pkg')

# D'abord, vérifions si scapy est disponible
try:
    from scapy.all import *
    print("scapy disponible")
except ImportError as e:
    print(f"scapy pas disponible: {e}")

# Vérifions aussi si pyshark est disponible
try:
    import pyshark
    print("pyshark disponible")
except ImportError as e:
    print(f"pyshark pas disponible: {e}")