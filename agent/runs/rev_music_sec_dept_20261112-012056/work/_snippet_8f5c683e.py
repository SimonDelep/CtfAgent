# Lire le fichier binaire
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher la séquence 81 66 81 6c 81 61 81 67 81 7b (flag{ avec préfixe 0x81)
flag_pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
flag_start = data.find(flag_pattern)
print("flag{ (pattern 0x81) position:", flag_start)

# Chercher s4lt26
salt_start = data.find(b's4lt26')
print("s4lt26 position:", salt_start)

if flag_start != -1:
    # Les données chiffrées sont entre la fin de flag{ et s4lt26
    # flag{ pattern fait 10 octets (5 chars * 2)
    encrypted_start = flag_start + len(flag_pattern)
    encrypted_data = data[encrypted_start:salt_start]
    
    print("Longueur des données chiffrées:", len(encrypted_data))
    print("Données chiffrées (hex):", encrypted_data.hex())
    
    # La clé est M4ch1n3_K3y!!
    key = b'M4ch1n3_K3y!!'
    print("Clé:", key)
    
    # Essayer XOR avec la clé
    decrypted = bytearray()
    for i, b in enumerate(encrypted_data):
        decrypted.append(b ^ key[i % len(key)])
    
    print("Décrypté (XOR simple):", decrypted)
    print("Décrypté (string):", decrypted.decode('latin-1', errors='replace'))
