#!/usr/bin/env python3
from scapy.all import *
import struct
from hashlib import sha256
from hmac import HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Données de session 1
client_random_1 = bytes.fromhex("6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a")
server_random_1 = bytes.fromhex("19f6457ff9167ca4cf4b004ebd4d5242ec4c2c97739f298e444f574e47524401")
master_secret_1 = bytes.fromhex("7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05")

# Données de session 2
client_random_2 = bytes.fromhex("6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd")
server_random_2 = bytes.fromhex("651629bfc08ac764f30974a420e52a577f1c1359632ecd86444f574e47524400")
master_secret_2 = bytes.fromhex("4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a63307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c")

def tls_prf(secret, label, seed, length):
    result = b""
    A = secret
    while len(result) < length:
        A = HMAC(secret, A, sha256).digest()
        result += HMAC(secret, A + seed, sha256).digest()
    return result[:length]

def derive_keys(master_secret, client_random, server_random):
    seed = client_random + server_random
    key_block = tls_prf(master_secret, b"key expansion", seed, 40)
    return (key_block[0:16], key_block[16:32], key_block[32:36], key_block[36:40])

cwk1, swk1, cwiv1, swiv1 = derive_keys(master_secret_1, client_random_1, server_random_1)
cwk2, swk2, cwiv2, swiv2 = derive_keys(master_secret_2, client_random_2, server_random_2)

# Charger le pcap
packets = rdpcap("capture.pcapng")

# Paquets Application Data identifiés:
# Session 1 (port 443): 16, 17, 20, 21, 22, 25, 26, 27, 28, 31, 33
# Session 2 (port 4433): 46, 47, 49, 50, 51, 52

def decrypt_app_data(pkt_idx, session_num):
    pkt = packets[pkt_idx]
    if Raw not in pkt:
        return None
    
    data = bytes(pkt[Raw].load)
    
    # TLS Header: content_type(1) + version(2) + length(2) = 5 bytes
    # Puis explicit_nonce (8 bytes) pour GCM
    # Puis ciphertext + tag (16 bytes)
    
    if len(data) < 5 + 8 + 16:
        return None
    
    content_type = data[0]
    version = data[1:3]
    length = struct.unpack("!H", data[3:5])[0]
    
    # Pour AES-GCM, le record contient: explicit_nonce (8) + ciphertext + tag (16)
    explicit_nonce = data[5:13]
    ciphertext_with_tag = data[13:]
    
    # Déterminer la clé et l'IV en fonction du sens
    # Client -> Server: utiliser client_write_key + client_write_iv
    # Server -> Client: utiliser server_write_key + server_write_iv
    
    if session_num == 1:
        # Session 1: port 443
        if pkt[TCP].sport == 443:  # Server -> Client
            key = swk1
            iv = swiv1
        else:  # Client -> Server
            key = cwk1
            iv = cwiv1
    else:
        # Session 2: port 4433
        if pkt[TCP].sport == 4433:  # Server -> Client
            key = swk2
            iv = cwiv2  # Note: pour session 2, vérifions
        else:  # Client -> Server
            key = cwk2
            iv = cwiv2
    
    # Nonce = IV (4 bytes) + explicit_nonce (8 bytes)
    nonce = iv + explicit_nonce
    
    # Décrypter avec AES-GCM
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
        return plaintext
    except Exception as e:
        return f"Error: {e}"

# Tester quelques paquets
print("=== Décryptage Session 1 ===")
for pkt_idx in [16, 17, 20]:
    result = decrypt_app_data(pkt_idx, 1)
    print(f"Paquet {pkt_idx}: {result[:100] if result else None}...")
    if result and isinstance(result, bytes):
        try:
            print(f"  Texte: {result.decode('utf-8', errors='replace')[:100]}")
        except:
            print(f"  Raw: {result[:50].hex()}")

print("\n=== Décryptage Session 2 ===")
for pkt_idx in [46, 47, 49]:
    result = decrypt_app_data(pkt_idx, 2)
    print(f"Paquet {pkt_idx}: {result[:100] if result else None}...")
    if result and isinstance(result, bytes):
        try:
            print(f"  Texte: {result.decode('utf-8', errors='replace')[:100]}")
        except:
            print(f"  Raw: {result[:50].hex()}")
