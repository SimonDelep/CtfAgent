#!/usr/bin/env python3
from hashlib import sha256
from hmac import HMAC

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

seed = client_random_1 + server_random_1
print(f"seed (CR + SR): {seed.hex()[:64]}...")

# Pour TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:
# key_block = PRF(master_secret, "key expansion", client_random + server_random, length)
# length = 2 * (key_length + iv_length) = 2 * (16 + 4) = 40 bytes

key_block = tls_prf(master_secret_1, b"key expansion", seed, 40)
print(f"key_block: {key_block.hex()}")
print(f"key_block length: {len(key_block)}")

# Décomposition:
# client_write_key (16) + server_write_key (16) + client_write_iv (4) + server_write_iv (4)
cwk = key_block[0:16]
swk = key_block[16:32]
cwiv = key_block[32:36]
swiv = key_block[36:40]

print(f"\ncclient_write_key: {cwk.hex()}")
print(f"server_write_key: {swk.hex()}")
print(f"client_write_iv: {cwiv.hex()}")
print(f"server_write_iv: {swiv.hex()}")

# Peut-être que l'ordre est différent?
# Selon RFC 5246, l'ordre est:
# client_write_MAC_key, server_write_MAC_key, client_write_key, server_write_key, client_write_IV, server_write_IV
# Mais pour AES-GCM, il n'y a pas de MAC, donc:
# client_write_key, server_write_key, client_write_IV, server_write_IV

# Vérifions si c'est peut-être l'inverse (server d'abord)
print("\n--- Hypothèse: ordre inversé ---")
cwk2 = key_block[0:16]
swk2 = key_block[16:32]
cwiv2 = key_block[32:36]
swiv2 = key_block[36:40]
print(f"client_write_key: {cwk2.hex()}")
print(f"server_write_key: {swk2.hex()}")

# Ou peut-être que le key_block est calculé avec un label différent?
# RFC 5246: label = "key expansion"
# Mais peut-être que c'est "master secret" ou autre?

# Essayons avec "master secret"
key_block2 = tls_prf(master_secret_1, b"master secret", seed, 40)
print(f"\nkey_block avec 'master secret': {key_block2.hex()}")
