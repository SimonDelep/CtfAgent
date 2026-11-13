try:
    from scapy.all import *
    print("scapy disponible")
except ImportError:
    print("scapy non disponible")