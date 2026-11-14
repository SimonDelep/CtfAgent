#!/usr/bin/env python3
"""
Décryptage TLS 1.2 avec PRF et AES-GCM
"""
import struct
from hashlib import sha256, sha1
from hmac import HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Données de la session 1 (d'après l'analyse précédente)
client_random = bytes.fromhex("6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a")
server_random = bytes.fromhex("19f6457f00000000000000000000000000000000000000000000000000000000")  # À ajuster
master_secret = bytes.fromhex("7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05")

# Pour la session 2
client_random_2 = bytes.fromhex("6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd")
master_secret_2 = bytes.fromhex("4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a663307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c")

print(f"Session 1 - CR: {client_random.hex()[:32]}...")
print(f"Session 1 - MS: {master_secret.hex()[:32]}...")
print(f"Session 2 - CR: {client_random_2.hex()[:32]}...")
print(f"Session 2 - MS: {master_secret_2.hex()[:32]}...")

# PRF TLS 1.2
def tls_prf(secret, label, seed, length):
    """PRF TLS 1.2 avec SHA256"""
    result = b""
    A = secret
    while len(result) < length:
        A = HMAC(secret, A, sha256).digest()
        result += HMAC(secret, A + seed, sha256).digest()
    return result[:length]

# Dérivation des clés pour AES-128-GCM
# Pour TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:
# - client_write_key: 16 bytes
# - server_write_key: 16 bytes
# - client_write_IV: 4 bytes (salt)
# - server_write_IV: 4 bytes (salt)

def derive_keys(master_secret, client_random, server_random):
    """Dérive les clés de chiffrement TLS 1.2"""
    seed = client_random + server_random
    
    # Pour AES-128-GCM: 2 clés de 16 bytes + 2 IVs de 4 bytes = 40 bytes
    key_block = tls_prf(master_secret, b"key expansion", seed, 40)
    
    client_write_key = key_block[0:16]
    server_write_key = key_block[16:32]
    client_write_iv = key_block[32:36]
    server_write_iv = key_block[36:40]
    
    return client_write_key, server_write_key, client_write_iv, server_write_iv

# Test avec session 1
cwk, swk, cwiv, swiv = derive_keys(master_secret, client_random, server_random)
print(f"\nSession 1 - client_write_key: {cwk.hex()}")
print(f"Session 1 - server_write_key: {swk.hex()}")
print(f"Session 1 - client_write_iv: {cwiv.hex()}")
print(f"Session 1 - server_write_iv: {swiv.hex()}")
