#!/usr/bin/env python3
"""
Décryptage TLS 1.2 AES-GCM avec calcul du salt
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

# Extraire Client Random et Server Random pour chaque session
def extract_session_info(packets):
    sessions = {}
    client_hello_info = {}
    
    for i, pkt in enumerate(packets):
        if Raw in pkt:
            raw = bytes(pkt[Raw].load)
            if len(raw) >= 5 and raw[0] == 0x16:
                handshake_type = raw[5]
                if handshake_type == 0x01:  # Client Hello
                    offset = 5 + 4 + 2
                    cr = raw[offset:offset+32]
                    client_hello_info[cr] = i
                elif handshake_type == 0x02:  # Server Hello
                    offset = 5 + 4 + 2
                    sr = raw[offset:offset+32]
                    # Le Server Hello contient aussi le Client Random? Non, juste Server Random
                    # Mais on peut mapper par ordre: premier Server Hello correspond au premier Client Hello
                    pass
    
    # Mapper les sessions: on suppose que les Client Hello et Server Hello sont appariés par ordre
    client_hellos = sorted(client_hello_info.items(), key=lambda x: x[1])
    
    # Trouver les Server Hellos
    server_hellos = {}
    for i, pkt in enumerate(packets):
        if Raw in pkt:
            raw = bytes(pkt[Raw].load)
            if len(raw) >= 5 and raw[0] == 0x16 and raw[5] == 0x02:
                offset = 5 + 4 + 2
                sr = raw[offset:offset+32]
                server_hellos[i] = sr
    
    # Associer chaque Client Hello avec le Server Hello suivant
    session_info = []
    last_ch_time = -1
    for cr, ch_time in client_hellos:
        # Trouver le Server Hello suivant
        for sh_time, sr in sorted(server_hellos.items()):
            if sh_time > ch_time:
                session_info.append((cr, sr, ch_time, sh_time))
                del server_hellos[sh_time]
                break
    
    return session_info

session_info = extract_session_info(packets)
print("Sessions trouvées:")
for cr, sr, ch_time, sh_time in session_info:
    print(f"  ClientHello@{ch_time}, ServerHello@{sh_time}")
    print(f"    CR: {cr.hex()}")
    print(f"    SR: {sr.hex()}")
    if cr in keys:
        ms = keys[cr]
        print(f"    MS: {ms.hex()}")
    else:
        print(f"    MS: (pas trouvé)")

# Pour TLS 1.2 GCM, le salt est calculé comme:
# client_write_IV = HKDF(master_secret, client_random || server_random, 4)
# Mais en pratique, pour TLS 1.2, le salt est souvent juste les 4 premiers bytes d'un dérivé

# Pour simplifier, essayons avec le salt = premiers 4 bytes du master_secret
# ou salt = premiers 4 bytes de hash(master_secret || client_random || server_random)

def compute_salt(master_secret, client_random, server_random):
    # Essayer différentes méthodes
    # Méthode 1: premiers 4 bytes du master_secret
    salt1 = master_secret[:4]
    
    # Méthode 2: hash SHA256 de (master_secret || client_random || server_random), premiers 4 bytes
    h = hashes.Hash(hashes.SHA256(), backend=default_backend())
    h.update(master_secret + client_random + server_random)
    salt2 = h.finalize()[:4]
    
    return salt1, salt2

for cr, sr, ch_time, sh_time in session_info:
    if cr in keys:
        ms = keys[cr]
        salt1, salt2 = compute_salt(ms, cr, sr)
        print(f"\nSession CR={cr.hex()[:16]}...")
        print(f"  Salt1 (MS[:4]): {salt1.hex()}")
        print(f"  Salt2 (SHA256[:4]): {salt2.hex()}")