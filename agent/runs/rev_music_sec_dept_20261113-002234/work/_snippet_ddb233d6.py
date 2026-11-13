with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Après flag{ (offset 124-132), il y a 0x81 0x0a à 134
# Puis 02 00 00 00 36 e5 17 bd... à partir de 136

# Le flag commence à 124 avec 0x81 0x66 = 'f'
# Décodons tout le flag en lisant les bytes 0x81 XX

flag_start = 124
flag_chars = []
i = flag_start
while i < len(data) - 1:
    if data[i] == 0x81:
        char_code = data[i+1]
        if 32 <= char_code < 127:
            flag_chars.append(chr(char_code))
        else:
            # Peut-être la fin du flag ou un caractère spécial
            flag_chars.append(f'[{char_code:02x}]')
        i += 2
    else:
        break

print("Flag décodé partiel:")
print(''.join(flag_chars))
print()

# Cherchons le '}' encodé (0x81 0x7d)
idx = data.find(bytes([0x81, 0x7d]))
print(f"Index de '}}' encodé (0x81 0x7d): {idx}")

# Si on ne trouve pas, cherchons la fin du flag dans les données chiffrées
# Le salt est à 182, donc le flag chiffré est entre 136 et 182
print(f"\nBytes entre flag{{ et salt: {data[136:182].hex()}")
print(f"Longueur: {182-136} bytes")