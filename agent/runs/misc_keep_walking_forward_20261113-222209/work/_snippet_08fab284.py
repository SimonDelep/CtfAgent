import sys
sys.path.insert(0, '/tmp/scapy_lib')
from scapy.all import *
from scapy.layers.tls.all import *
import binascii

# Lire les clés du log
keys = {}
with open('vcheck.log', 'r') as f:
    for line in f:
        if line.startswith('CLIENT_RANDOM'):
            parts = line.strip().split()
            client_random = parts[1]
            master_secret = parts[2]
            keys[client_random] = master_secret
            print(f"Client Random: {client_random}")
            print(f"Master Secret: {master_secret}")

print(f"\nTotal clés: {len(keys)}")