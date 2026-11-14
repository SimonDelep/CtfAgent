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

print(f"client_write_key: {cwk1.hex()}")
print(f"server_write_key: {swk1.hex()}")
print(f"client_write_iv (salt): {cwiv1.hex()}")
print(f"server_write_iv (salt): {swiv1.hex()}")

# Le paquet 16 est Client -> Server (sport=60437, dport=443)
# Donc on devrait utiliser client_write_key et client_write_iv

# En TLS 1.2 GCM, le nonce est: salt (4) + sequence_number (8)
# Le sequence_number est un compteur qui commence à 0 pour chaque session

# Peut-être que l'explicit_nonce dans le paquet EST le sequence_number?
# Ou peut-être que le salt est différent?

# Essayons avec juste le salt comme nonce (4 bytes)
packets = rdpcap("capture.pcapng")
pkt = packets[16]
data = bytes(pkt[Raw].load)
explicit_nonce = data[5:13]
ciphertext_with_tag = data[13:]

print(f"\nexplicit_nonce: {explicit_nonce.hex()}")

# Essayer avec salt seul (4 bytes) comme nonce
nonce_salt_only = cwiv1
print(f"Trying nonce = salt only: {nonce_salt_only.hex()}")
try:
    aesgcm = AESGCM(cwk1)
    plaintext = aesgcm.decrypt(nonce_salt_only, ciphertext_with_tag, None)
    print(f"Success! {plaintext[:100]}")
except Exception as e:
    print(f"Error: {e}")

# Peut-être que le salt est en fait les 4 premiers bytes du master_secret?
# Ou dérivé différemment?

# Vérifions la RFC 5288 pour AES-GCM en TLS 1.2
# nonce_explicit = 8 bytes (dans le record)
# nonce = salt (4 bytes) + nonce_explicit (8 bytes) = 12 bytes

# Mais peut-être que dans cette implémentation, le salt est différent?
# Essayons avec explicit_nonce comme nonce (8 bytes) sans salt
print(f"\nTrying nonce = explicit_nonce only: {explicit_nonce.hex()}")
try:
    aesgcm = AESGCM(cwk1)
    plaintext = aesgcm.decrypt(explicit_nonce, ciphertext_with_tag, None)
    print(f"Success! {plaintext[:100]}")
except Exception as e:
    print(f"Error: {e}")

# Ou peut-être que le salt est le server_random ou client_random?
# Essayons avec les 4 premiers bytes de client_random
nonce_cr = client_random_1[:4]
print(f"\nTrying nonce = client_random[:4] + explicit_nonce: {nonce_cr.hex() + explicit_nonce.hex()}")
try:
    aesgcm = AESGCM(cwk1)
    plaintext = aesgcm.decrypt(nonce_cr + explicit_nonce, ciphertext_with_tag, None)
    print(f"Success! {plaintext[:100]}")
except Exception as e:
    print(f"Error: {e}")
