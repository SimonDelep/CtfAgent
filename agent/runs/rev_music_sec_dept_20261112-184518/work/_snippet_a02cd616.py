with open('session.bin', 'rb') as f:
    data = f.read()

# Cherchons 'flag{' en cherchant 0x81 suivi de 'f', 'l', 'a', 'g', '{'
# 'f' = 0x66, 'l' = 0x6c, 'a' = 0x61, 'g' = 0x67, '{' = 0x7b

# Cherchons le pattern 0x81 0x66 0x81 0x6c 0x81 0x61 0x81 0x67 0x81 0x7b
pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
print(f"Pattern recherché: {pattern.hex()}")

idx = data.find(pattern)
print(f"Offset trouvé: {idx} (0x{idx:x})")

if idx >= 0:
    # Extraire et décoder
    # Le pattern est 0x81 + char, donc on prend chaque paire
    encoded = data[idx:idx+10]
    print(f"Bytes encodés: {encoded.hex()}")
    
    # Décode: chaque paire est 0x81 suivi du caractère
    decoded = ''.join(chr(data[idx + 2*i + 1]) for i in range(5))
    print(f"Décodé: {decoded}")
    
    # Regardons ce qui suit
    print(f"\nDonnées après 'flag{{':")
    print(' '.join(f'{b:02x}' for b in data[idx+10:idx+40]))
    
    # Après 'flag{', on a 0x81 0x0a (newline), puis 0x02 0x00 0x00 0x00
    # Puis le ciphertext commence
    
    # Trouver le début du ciphertext
    after_flag = idx + 10  # Après 'flag{'
    print(f"\nOffset après 'flag{{': {after_flag} (0x{after_flag:x})")
    print(f"Données: {data[after_flag:after_flag+20].hex()}")
    
    # 0x81 0x0a = newline encodé
    # 0x02 0x00 0x00 0x00 = peut-être une longueur
    # Puis le ciphertext
    
    # Trouver où commence vraiment le ciphertext
    # Après 'flag{\\n' (0x81 0x66 0x81 0x6c 0x81 0x61 0x81 0x67 0x81 0x7b 0x81 0x0a)
    # On a 0x02 0x00 0x00 0x00
    # Puis le ciphertext
    
    ciphertext_start = after_flag + 2 + 4  # Après 0x81 0x0a et 0x02 0x00 0x00 0x00
    print(f"\nCiphertext start: {ciphertext_start} (0x{ciphertext_start:x})")
    print(f"Ciphertext: {data[ciphertext_start:ciphertext_start+30].hex()}")
    
    # Cherchons 's4lt26'
    salt_offset = data.find(b's4lt26')
    print(f"\nOffset de 's4lt26': {salt_offset} (0x{salt_offset:x})")
    
    # Le salt est répété plusieurs fois
    # Essayons de déchiffrer le ciphertext avec XOR en utilisant 's4lt26'
    salt = b's4lt26'
    ciphertext = data[ciphertext_start:ciphertext_start+30]
    
    decrypted = []
    for i, b in enumerate(ciphertext):
        decrypted.append(b ^ salt[i % len(salt)])
    
    print(f"Décrypté (XOR avec salt): {''.join(chr(b) if 32 <= b < 127 else '.' for b in decrypted)}")
    print(f"Bytes: {bytes(decrypted).hex()}")
