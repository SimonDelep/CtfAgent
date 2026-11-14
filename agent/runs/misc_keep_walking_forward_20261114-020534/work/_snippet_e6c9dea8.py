#!/usr/bin/env python3
"""
Décryptage TLS 1.2 AES-GCM - Décrypter les paquets Application Data
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

# Extraire les informations de session
def extract_session_info(packets):
    client_hello_info = {}
    server_hello_info = {}
    
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
                    server_hello_info[i] = sr
    
    client_hellos = sorted(client_hello_info.items(), key=lambda x: x[1])
    session_info = []
    
    for cr, ch_time in client_hellos:
        for sh_time, sr in sorted(server_hello_info.items()):
            if sh_time > ch_time:
                ms = keys.get(cr)
                if ms:
                    session_info.append({'cr': cr, 'sr': sr, 'ms': ms, 'ch_time': ch_time, 'sh_time': sh_time})
                break
    
    return session_info

sessions = extract_session_info(packets)

# Calculer le salt pour chaque session (méthode standard TLS 1.2)
# Pour GCM, le client_write_iv est dérivé
# Simplification: salt = premiers 4 bytes du master_secret
def get_salt(master_secret):
    return master_secret[:4]

# Décrypter un paquet Application Data
def decrypt_tls_record(raw, salt, master_secret):
    # Header TLS: Type(1) + Version(2) + Length(2) = 5 bytes
    # Puis: explicit_nonce (8) + ciphertext + tag (16)
    if len(raw) < 5 + 8 + 16:
        return None
    
    # Length field
    length = struct.unpack('>H', raw[3:5])[0]
    
    # explicit_nonce
    explicit_nonce = raw[5:13]
    
    # ciphertext + tag
    encrypted_data = raw[13:]
    
    # Tag est les 16 derniers bytes
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[:-16]
    
    # Nonce = salt (4) + explicit_nonce (8) = 12 bytes
    nonce = salt + explicit_nonce
    
    # Décrypter avec AES-128-GCM
    # master_secret est 48 bytes pour TLS 1.2 (AES-128)
    # La clé de chiffrement est dérivée du master_secret
    # Pour simplifier, essayons avec master_secret[:16] comme clé
    
    key = master_secret[:16]  # AES-128
    
    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext
    except Exception as e:
        return f"Error: {e}"

# Trouver et décrypter les paquets Application Data
for session in sessions:
    print(f"\n=== Session CR={session['cr'].hex()[:16]}... ===")
    salt = get_salt(session['ms'])
    print(f"Salt: {salt.hex()}")
    
    for i, pkt in enumerate(packets):
        if Raw in pkt:
            raw = bytes(pkt[Raw].load)
            if len(raw) >= 5 and raw[0] == 0x17:  # Application Data
                plaintext = decrypt_tls_record(raw, salt, session['ms'])
                if plaintext:
                    print(f"\nPaquet {i}:")
                    if isinstance(plaintext, bytes):
                        try:
                            text = plaintext.decode('utf-8', errors='replace')
                            print(f"  Plaintext: {text[:200]}")
                        except:
                            print(f"  Plaintext (hex): {plaintext[:100].hex()}")
                    else:
                        print(f"  {plaintext}")