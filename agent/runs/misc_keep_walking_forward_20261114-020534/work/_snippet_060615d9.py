#!/usr/bin/env python3
"""
Décryptage TLS 1.2 AES-GCM - Correction extraction Client Random
"""
from scapy.all import rdpcap, Raw
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
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
print("Clés du log:")
for cr, ms in keys.items():
    print(f"  CR: {cr.hex()}")
    print(f"  MS: {ms.hex()}")

# Extraire le Client Random du Client Hello (32 bytes après la version)
def get_client_random_from_client_hello(raw):
    # Header TLS: Type(1) + Version(2) + Length(2) = 5 bytes
    # Handshake: Type(1) + Length(3) = 4 bytes
    # Puis: Version(2) + Random(32)
    offset = 5 + 4 + 2  # 11 bytes pour aller au début du Random
    if len(raw) >= offset + 32:
        return raw[offset:offset+32]
    return None

# Extraire le Server Random du Server Hello
def get_server_random_from_server_hello(raw):
    offset = 5 + 4 + 2  # 11 bytes
    if len(raw) >= offset + 32:
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

# Vérifier correspondance
print("\nCorrespondance:")
for cr_pcap in client_randoms_in_pcap:
    if cr_pcap in keys:
        print(f"  MATCH: {cr_pcap.hex()[:16]}...")
    else:
        print(f"  PAS MATCH: {cr_pcap.hex()[:16]}...")