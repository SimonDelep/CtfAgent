try:
    import pyshark
    print("pyshark disponible")
except ImportError:
    print("pyshark non disponible")
try:
    import dpkt
    print("dpkt disponible")
except ImportError:
    print("dpkt non disponible")