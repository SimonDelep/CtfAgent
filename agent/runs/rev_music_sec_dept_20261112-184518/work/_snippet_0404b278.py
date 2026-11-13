with open('session.bin', 'rb') as f:
    data = f.read()

# Le flag commence à 0x7c avec "flag{"
# Après 0x85 ('{'), il y a 0x81 0x0a (LF encodé), puis 0x02 0x00 0x00 0x00
# Puis des données chiffrées de 0x8c à ...
# Le '_' est à 0xab

# Essayons de déchiffrer les données entre 0x8c et 0xab avec XOR
ciphertext = data[0x8c:0xab]
print("Ciphertext (0x8c-0xab):", ciphertext.hex())

# La clé est "M4ch1n3_K3y!!" (13 bytes)
key = b"M4ch1n3_K3y!!"
salt = b"s4lt26"

# Essayons XOR avec la clé
def xor_decrypt(ct, key):
    result = []
    for i, b in enumerate(ct):
        result.append(b ^ key[i % len(key)])
    return bytes(result)

print("\nXOR avec clé 'M4ch1n3_K3y!!':")
print(xor_decrypt(ciphertext, key))

print("\nXOR avec salt 's4lt26':")
print(xor_decrypt(ciphertext, salt))

# Peut-être que le salt est utilisé différemment
# Essayons avec le salt répété
print("\nXOR avec salt répété:")
print(xor_decrypt(ciphertext, salt * 4))