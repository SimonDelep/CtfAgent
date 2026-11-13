import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Essayons ROT13
def rot13(s):
    result = ''
    for c in s:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + 13) % 26 + base)
        else:
            result += c
    return result

print(f"ROT13: {rot13(decoded)}")

# Essayons de voir si c'est un XOR avec la position
result = ''
for i, c in enumerate(decoded):
    result += chr(ord(c) ^ (i % 256))
print(f"XOR position: {result}")

# Peut-être que le message est déjà correct et qu'il faut juste le soumettre tel quel?
# Ou peut-être que c'est un autre encodage

# Essayons Atbash pour les lettres
def atbash(s):
    result = ''
    for c in s:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr(base + (25 - (ord(c) - base)))
        else:
            result += c
    return result

print(f"Atbash: {atbash(decoded)}")