with open('session.bin', 'rb') as f:
    data = f.read()

# Le ciphertext commence à 0x8c
# Regardons la structure complète autour du flag

# Offset 0x7c: 'flag{' encodé
# Offset 0x86: 0x81 0x0a (newline)
# Offset 0x88: 0x02 0x00 0x00 0x00 (peut-être une longueur ou un compteur)
# Offset 0x8c: ciphertext

# Combien d'octets de ciphertext ?
# Regardons jusqu'à ce qu'on trouve 's4lt26'
salt_offset = data.find(b's4lt26')
print(f"Salt offset: {salt_offset} (0x{salt_offset:x})")

# Le ciphertext va de 0x8c à 0xb6 (avant 's4lt26')
ciphertext_len = salt_offset - 0x8c
print(f"Ciphertext length: {ciphertext_len} octets")

ciphertext = data[0x8c:salt_offset]
print(f"Ciphertext: {ciphertext.hex()}")

# 's4lt26' est répété plusieurs fois
# Regardons combien de fois
count = 0
pos = 0
while True:
    idx = data.find(b's4lt26', pos)
    if idx == -1:
        break
    count += 1
    pos = idx + 1
print(f"'s4lt26' apparaît {count} fois")

# Regardons ce qui suit 's4lt26'
print(f"\nDonnées après 's4lt26':")
print(' '.join(f'{b:02x}' for b in data[salt_offset: salt_offset+50]))

# Après 's4lt26', on voit 'v2rom: strip!M4ch1n3_K3y!!'
# Peut-être que 'M4ch1n3_K3y!!' est la clé ?

# Cherchons 'M4ch1n3_K3y!!'
key_start = data.find(b'M4ch1n3_K3y!!')
print(f"\nOffset de 'M4ch1n3_K3y!!': {key_start} (0x{key_start:x})")

if key_start >= 0:
    key = data[key_start:key_start+13]
    print(f"Clé potentielle: {key}")
    
    # Essayons de déchiffrer avec cette clé
    decrypted = []
    for i, b in enumerate(ciphertext):
        decrypted.append(b ^ key[i % len(key)])
    
    print(f"Décrypté (XOR avec M4ch1n3_K3y!!): {''.join(chr(b) if 32 <= b < 127 else '.' for b in decrypted)}")
