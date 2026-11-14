#!/usr/bin/env python3
"""
Décryptage TLS manuel avec Scapy et cryptography
"""
from scapy.all import rdpcap, Raw
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

# Lire le pcap
packets = rdpcap('capture.pcapng')

# Extraire les clés du log
def parse_keys(log_file):
    keys = {}
    with open(log_file, 'r') as f:
        for line in f:
            if line.startswith('CLIENT_RANDOM'):
                parts = line.strip().split()
                client_random = parts[1]
                master_secret = parts[2]
                keys[client_random] = master_secret
    return keys

keys = parse_keys('vcheck.log')
print("Clés trouvées:")
for cr, ms in keys.items():
    print(f"  ClientRandom: {cr[:16]}... -> MasterSecret: {ms[:16]}...")

# Trouver les paquets TLS Application Data (type 0x17)
# TLS Record: Content Type (1) + Version (2) + Length (2) + Payload
tls_records = []
for i, pkt in enumerate(packets):
    if Raw in pkt:
        raw = bytes(pkt[Raw].load)
        # Vérifier si c'est du TLS (Content Type en premier octet)
        if len(raw) >= 5:
            content_type = raw[0]
            if content_type == 0x17:  # Application Data
                tls_records.append((i, raw))
                print(f"Paquet {i}: Application Data, len={len(raw)}")

print(f"\nTotal {len(tls_records)} paquets Application Data trouvés")