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

packets = rdpcap("capture.pcapng")

# Analyser le paquet 16 en détail
pkt = packets[16]
data = bytes(pkt[Raw].load)

print(f"Paquet 16:")
print(f"  sport={pkt[TCP].sport}, dport={pkt[TCP].dport}")
print(f"  Raw data length: {len(data)}")
print(f"  First 20 bytes: {data[:20].hex()}")

# TLS Header
content_type = data[0]
version = data[1:3]
length = struct.unpack("!H", data[3:5])[0]
print(f"  content_type=0x{content_type:02x}, version=0x{version.hex()}, length={length}")

# Pour TLS 1.2 avec AES-GCM:
# - Header TLS: 5 bytes
# - explicit_nonce: 8 bytes
# - ciphertext + tag (16 bytes)

explicit_nonce = data[5:13]
ciphertext_with_tag = data[13:]
print(f"  explicit_nonce: {explicit_nonce.hex()}")
print(f"  ciphertext_with_tag length: {len(ciphertext_with_tag)}")

# Essayer avec client_write_key (Client -> Server)
# Nonce = IV (4 bytes) + explicit_nonce (8 bytes)
nonce = cwiv1 + explicit_nonce
print(f"  nonce (IV + explicit): {nonce.hex()}")

aesgcm = AESGCM(cwk1)
try:
    plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
    print(f"  Décrypté avec cwk1: {plaintext[:100]}")
except Exception as e:
    print(f"  Erreur avec cwk1: {e}")

# Essayer avec server_write_key
try:
    plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
    print(f"  Décrypté avec swk1: {plaintext[:100]}")
except Exception as e:
    print(f"  Erreur avec swk1: {e}")

# Peut-être que le nonce est juste explicit_nonce (8 bytes) sans IV préfixé?
nonce2 = explicit_nonce
try:
    plaintext = aesgcm.decrypt(nonce2, ciphertext_with_tag, None)
    print(f"  Décrypté avec nonce=explicit_only: {plaintext[:100]}")
except Exception as e:
    print(f"  Erreur avec nonce=explicit_only: {e}")

# Ou peut-être que le salt est utilisé différemment?
# Dans TLS 1.2, le nonce pour GCM est: nonce = salt (4) + explicit_nonce (8)
# Mais peut-être que le salt est dérivé différemment?
