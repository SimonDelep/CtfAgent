import struct

# Lire le fichier binaire
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Trouver les positions
flag_start = data.find(b'flag{')
salt_start = data.find(b's4lt26')

print("flag{ position:", flag_start)
print("s4lt26 position:", salt_start)

# Extraire les données chiffrées entre flag{ et s4lt26
# flag{ est de 5 octets, donc données chiffrées commencent à flag_start + 5
encrypted_start = flag_start + 5
encrypted_data = data[encrypted_start:salt_start]

print("Longueur des données chiffrées:", len(encrypted_data))
print("Données chiffrées (hex):", encrypted_data.hex())

# La clé est M4ch1n3_K3y!!
key = b'M4ch1n3_K3y!!'
print("Clé:", key)
print("Longueur clé:", len(key))

# Essayer XOR avec la clé
decrypted = bytearray()
for i, b in enumerate(encrypted_data):
    decrypted.append(b ^ key[i % len(key)])

print("Décrypté (XOR simple):", decrypted)
print("Décrypté (string):", decrypted.decode('latin-1', errors='replace'))
