# La clé est \xaa\xc4\xc3D (4 octets)
key = bytes([0xaa, 0xc4, 0xc3, 0x44])
print(f"Clé: {key!r}")

# Le texte à décoder est '2_5t3@1_'
text = b'2_5t3@1_'
print(f"Texte: {text!r}")

# XOR avec la clé (répétée)
result = bytes([text[i] ^ key[i % len(key)] for i in range(len(text))])
print(f"XOR avec clé: {result!r}")

# Essayons aussi l'inverse : XOR de la clé avec le texte
result2 = bytes([key[i % len(key)] ^ text[i] for i in range(len(text))])
print(f"XOR inverse: {result2!r}")

# Peut-être que le flag est juste '2_5t3@1_'
print(f"\nHypothèse: csaw{{2_5t3@1_}}")