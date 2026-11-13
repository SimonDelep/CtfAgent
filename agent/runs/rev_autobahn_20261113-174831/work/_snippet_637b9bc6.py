# smc_key.0 est à l'adresse 0x4020a8, taille 8 octets
# C'est dans .rodata (adresse 0x402000, offset 0x2000)
# Donc l'offset dans le fichier est: 0x2000 + (0x4020a8 - 0x402000) = 0x2000 + 0xa8 = 0x20a8

with open('nitro', 'rb') as f:
    data = f.read()

# Lire smc_key.0 (8 octets à l'offset 0x20a8)
smc_key_offset = 0x20a8
smc_key = data[smc_key_offset:smc_key_offset+8]
print(f"smc_key.0 à offset 0x{smc_key_offset:x}: {smc_key.hex()}")
print(f"Valeur (little-endian): {int.from_bytes(smc_key, 'little')}")
print(f"Valeur (big-endian): {int.from_bytes(smc_key, 'big')}")

# Maintenant, analysons la section enccode
# Adresse virtuelle: 0x40130d, offset: 0x130d, taille: 0x15e (350 octets)
enccode_offset = 0x130d
enccode_size = 0x15e
enccode = data[enccode_offset:enccode_offset+enccode_size]

print(f"\n=== Section enccode (offset 0x{enccode_offset:x}, taille {enccode_size}) ===")
print(f"Premiers 64 octets: {enccode[:64].hex()}")

# Essayer de déchiffrer avec XOR simple en utilisant smc_key
# Peut-être que la clé est répétée ou utilisée différemment
print("\n=== Tentative de déchiffrement XOR ===")

# Option 1: XOR avec chaque octet de la clé tour à tour
def xor_decrypt(ciphertext, key):
    result = bytearray()
    for i, b in enumerate(ciphertext):
        result.append(b ^ key[i % len(key)])
    return bytes(result)

decrypted = xor_decrypt(enccode, smc_key)
print("Décrypté avec XOR (clé répétée):")
print(decrypted[:100])

# Option 2: Peut-être que smc_key est un pointeur vers la clé réelle
# Regardons la valeur de smc_key comme adresse
key_value = int.from_bytes(smc_key, 'little')
print(f"\nValeur de smc_key comme adresse: 0x{key_value:x}")

# Si c'est une adresse, elle pointe vers quelque chose dans le binaire
# Mais 0x... peut être une adresse virtuelle