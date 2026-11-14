#!/usr/bin/env python3
"""
Décryptage TLS 1.2 AES-GCM
"""
from scapy.all import rdpcap, Raw
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import struct

packets = rdpcap('capture.pcapng')

# Extraire les clés du log
def parse_keys(log_file):
    keys = {}
    with open(log_file, 'r') as f:
        for line in f:
            if line.startswith('CLIENT_RANDOM'):
                parts = line.strip().split()
                client_random = bytes.fromhex(parts[1])
                master_secret = bytes.fromhex(parts[2])
                keys[client_random] = master_secret
    return keys

keys = parse_keys('vcheck.log')

# Extraire le Client Random du Client Hello pour mapper les clés
def get_client_random_from_client_hello(raw):
    # Client Hello: Handshake Type(1) + Length(3) + Version(2) + Random(32) + ...
    # Après header TLS (5 bytes) + handshake type (1) + handshake length (3)
    offset = 5 + 1 + 3
    if len(raw) >= offset + 34:
        return raw[offset:offset+32]
    return None

# Extraire le Server Random du Server Hello
def get_server_random_from_server_hello(raw):
    offset = 5 + 1 + 3
    if len(raw) >= offset + 34:
        return raw[offset:offset+32]
    return None

# Trouver les Client Randoms dans le pcap
client_randoms_in_pcap = {}
for i, pkt in enumerate(packets):
    if Raw in pkt:
        raw = bytes(pkt[Raw].load)
        if len(raw) >= 5 and raw[0] == 0x16:  # Handshake
            handshake_type = raw[5]
            if handshake_type == 0x01:  # Client Hello
                cr = get_client_random_from_client_hello(raw)
                if cr:
                    client_randoms_in_pcap[cr] = i
                    print(f"Paquet {i}: Client Hello, ClientRandom: {cr.hex()}")

# Trouver les Server Randoms
server_randoms_in_pcap = {}
for i, pkt in enumerate(packets):
    if Raw in pkt:
        raw = bytes(pkt[Raw].load)
        if len(raw) >= 5 and raw[0] == 0x16:  # Handshake
            handshake_type = raw[5]
            if handshake_type == 0x02:  # Server Hello
                sr = get_server_random_from_server_hello(raw)
                if sr:
                    server_randoms_in_pcap[sr] = i
                    print(f"Paquet {i}: Server Hello, ServerRandom: {sr.hex()}")

print(f"\n{len(client_randoms_in_pcap)} Client Hello trouvés")
print(f"{len(server_randoms_in_pcap)} Server Hello trouvés")