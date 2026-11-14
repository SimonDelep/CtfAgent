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
    """PRF TLS 1.2 avec SHA256"""
    result = b""
    A = secret
    while len(result) < length:
        A = HMAC(secret, A, sha256).digest()
        result += HMAC(secret, A + seed, sha256).digest()
    return result[:length]

def derive_keys(master_secret, client_random, server_random):
    """Dérive les clés de chiffrement TLS 1.2 pour AES-128-GCM"""
    seed = client_random + server_random
    
    # Pour AES-128-GCM: 2 clés de 16 bytes + 2 IVs de 4 bytes = 40 bytes
    key_block = tls_prf(master_secret, b"key expansion", seed, 40)
    
    client_write_key = key_block[0:16]
    server_write_key = key_block[16:32]
    client_write_iv = key_block[32:36]
    server_write_iv = key_block[36:40]
    
    return client_write_key, server_write_key, client_write_iv, server_write_iv

# Dérivation des clés
cwk1, swk1, cwiv1, swiv1 = derive_keys(master_secret_1, client_random_1, server_random_1)
cwk2, swk2, cwiv2, swiv2 = derive_keys(master_secret_2, client_random_2, server_random_2)

print("=== Session 1 ===")
print(f"client_write_key: {cwk1.hex()}")
print(f"server_write_key: {swk1.hex()}")
print(f"client_write_iv (salt): {cwiv1.hex()}")
print(f"server_write_iv (salt): {swiv1.hex()}")

print("\n=== Session 2 ===")
print(f"client_write_key: {cwk2.hex()}")
print(f"server_write_key: {swk2.hex()}")
print(f"client_write_iv (salt): {cwiv2.hex()}")
print(f"server_write_iv (salt): {swiv2.hex()}")
