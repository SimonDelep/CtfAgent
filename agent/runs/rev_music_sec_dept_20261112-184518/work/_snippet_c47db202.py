# Essayer de décoder le flag avec XOR
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Le flag chiffré commence à 0x8c
cipher_start = 0x8c
cipher_data = data[cipher_start:cipher_start+50]

# Salt est "s4lt26" à l'offset 0xb6
salt = data[0xb6:0xb6+6]
print(f"Salt: {salt}")

# Clé est "M4ch1n3_K3y!!" à l'offset 0xeb
key = data[0xeb:0xeb+13]
print(f"Key: {key}")

# Essayons XOR avec le salt répété
print("\nXOR avec salt 's4lt26':")
result = []
for i, b in enumerate(cipher_data):
    result.append(b ^ salt[i % len(salt)])
print(bytes(result))

# Essayons XOR avec la clé
print("\nXOR avec key 'M4ch1n3_K3y!!':")
result = []
for i, b in enumerate(cipher_data):
    result.append(b ^ key[i % len(key)])
print(bytes(result))

# Peut-être que le flag est XOR avec un décalage basé sur la position
print("\nXOR avec position (i % 256):")
result = []
for i, b in enumerate(cipher_data):
    result.append(b ^ i)
print(bytes(result))