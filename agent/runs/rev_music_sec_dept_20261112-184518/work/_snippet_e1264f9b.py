with open('session.bin', 'rb') as f:
    data = f.read()

# L'offset de 'flag{' encodé est 0x80 + 2 = 0x82 (car 80 ff 81...)
# En fait, regardons plus précisément
# 0x80: 80 ff 81 66 81 6c 81 61 81 67 81 7b
# Donc 'flag{' commence à l'offset 0x82

# Décode le flag encodé
start = 0x82
end = start + 5  # 'flag{'
encoded_flag = data[start:end]
print(f"Encoded flag bytes: {encoded_flag.hex()}")

# Décode chaque octet en soustrayant 0x81
decoded = ''.join(chr(b - 0x81) for b in encoded_flag)
print(f"Decoded: {decoded}")

# Maintenant, regardons ce qui suit 'flag{'
# Après 'flag{' (5 octets encodés = 5 octets), on a 81 0a 02 00 00 00...
# 81 0a = '\n' encodé
# 02 00 00 00 = peut-être une longueur ou un compteur

# Le ciphertext commence après cela
# Regardons à partir de l'offset 0x8a (après 'flag{\\n\\x02\\x00\\x00\\x00')
# En fait, 0x82 + 5*2 = 0x82 + 10 = 0x8c pour le début du ciphertext

# Mais attendons, chaque caractère encodé prend 1 octet (0x81 + ASCII)
# Donc 'flag{' = 5 octets: 0x82 à 0x86
# Puis 81 0a = '\n' à 0x87
# Puis 02 00 00 00 à 0x88-0x8b
# Puis le ciphertext commence à 0x8c

print(f"\nDonnées à partir de 0x8c:")
print(' '.join(f'{b:02x}' for b in data[0x8c:0x8c+50]))

# Le ciphertext semble être: 36 e5 17 bd 6e 0b 4e 8c 73 ed 60 16 74 a6 2a 90 31 a4 7a 8b...
# Et il y a 's4lt26' répété plus loin

# Essayons de déchiffrer avec XOR en utilisant 's4lt26' comme clé
salt = b's4lt26'
ciphertext = data[0x8c:0x8c+30]  # Prendre un peu de ciphertext

print(f"\nCiphertext: {ciphertext.hex()}")
print(f"Salt: {salt}")

# XOR avec le salt répété
decrypted = []
for i, b in enumerate(ciphertext):
    decrypted.append(b ^ salt[i % len(salt)])

print(f"Décrypté (XOR avec salt): {''.join(chr(b) if 32 <= b < 127 else '.' for b in decrypted)}")
print(f"Bytes: {bytes(decrypted).hex()}")
