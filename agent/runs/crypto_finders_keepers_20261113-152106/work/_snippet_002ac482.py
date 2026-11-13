import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Essayons XOR avec différentes clés
# Peut-être que c'est XOR avec une clé simple
for key in range(256):
    result = ''.join(chr(ord(c) ^ key) for c in decoded)
    if result.startswith('csaw{'):
        print(f"XOR avec {key}: {result}")

# Ou peut-être un décalage ROT sur chaque caractère
# Essayons ROT13
import codecs
rot13 = codecs.decode(decoded, 'rot_13')
print(f"ROT13: {rot13}")

# Essayons de voir si c'est un décalage constant
for shift in range(26):
    result = ''
    for c in decoded:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    if 'csaw' in result.lower():
        print(f"ROT{shift}: {result}")