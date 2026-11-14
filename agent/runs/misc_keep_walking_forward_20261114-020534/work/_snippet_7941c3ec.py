from scapy.all import *
import binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

# Lire les clés du log
def parse_sslkeys(log_file):
    keys = {}
    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[0] == 'CLIENT_RANDOM':
                client_random = parts[1]
                master_secret = parts[2]
                keys[client_random] = master_secret
    return keys

keys = parse_sslkeys('vcheck.log')
print("Clés trouvées:")
for cr, ms in keys.items():
    print(f"  CLIENT_RANDOM: {cr}")
    print(f"  Master Secret: {ms}")
    print()

# TLS 1.2 PRF pour dériver les clés
# Pour AES-GCM, on a besoin de:
# - client_write_key, server_write_key (16 bytes pour AES-128, 32 pour AES-256)
# - client_write_IV, server_write_IV (12 bytes pour GCM)

def tls_prf(secret, label, seed, length):
    """TLS 1.2 PRF avec SHA256"""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
    # Simplifié: on utilise HMAC-SHA256 en cascade
    result = b''
    a = seed
    while len(result) < length:
        # P_hash(secret, a + seed)
        h = hashes.Hash(hashes.SHA256(), backend=default_backend())
        h.update(secret.encode('hex') if isinstance(secret, str) else secret)
        h.update(a)
        b = h.finalize()
        a = b  # Pour simplifier, on réutilise b comme a
        result += b
    return result[:length]

# En fait, pour TLS 1.2, la dérivation de clés est plus complexe
# Utilisons la méthode standard
from hashlib import sha256
import hmac

def tls_prf_sha256(secret, label, seed, length):
    """TLS 1.2 PRF avec SHA256"""
    if isinstance(secret, str):
        secret = bytes.fromhex(secret)
    if isinstance(label, str):
        label = label.encode()
    if isinstance(seed, str):
        seed = bytes.fromhex(seed)
    
    result = b''
    a = seed
    while len(result) < length:
        # HMAC-SHA256(secret, a + seed)
        b = hmac.new(secret, a + seed, sha256).digest()
        a = b
        result += b
    return result[:length]

# Pour AES-128-GCM:
# key_block = PRF(master_secret, "key expansion", server_random + client_random)
# Puis on extrait:
# - client_write_key (16 bytes)
# - server_write_key (16 bytes)
# - client_write_iv (4 bytes, mais en GCM c'est 12 bytes avec expansion)
# - server_write_iv (4 bytes)

# D'abord, extraire les server_random des paquets
packets = rdpcap('capture.pcapng')

# Trouver le Client Hello et Server Hello pour obtenir les randoms
for i, pkt in enumerate(packets):
    if pkt.haslayer('TCP') and pkt.haslayer('Raw'):
        raw = bytes(pkt['Raw'].load)
        if len(raw) >= 43:  # Client Hello minimum
            content_type = raw[0]
            if content_type == 0x16:  # Handshake
                handshake_type = raw[5]
                if handshake_type == 0x01:  # Client Hello
                    # Client Hello: random est à offset 6+4=10 (après header)
                    client_random = raw[6:38]  # 32 bytes
                    print(f"Paquet {i}: Client Hello, client_random = {binascii.hexlify(client_random).decode()}")
                elif handshake_type == 0x02:  # Server Hello
                    server_random = raw[6:38]
                    print(f"Paquet {i}: Server Hello, server_random = {binascii.hexlify(server_random).decode()}")
                    # Vérifier DOWNGRD signature
                    if b'DOWNGRD' in raw:
                        print(f"  -> DOWNGRD trouvé!")