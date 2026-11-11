import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Original decoded: {decoded}")

# Essayons ROT13
def rot13(s):
    result = []
    for c in s:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

print(f"ROT13: {rot13(decoded)}")

# Peut-être que le base64 lui-même est double encodé ?
# Ou peut-être que c'est un XOR avec une clé répétitive
# Essayons XOR avec différentes clés

def xor_with_key(s, key):
    result = []
    for i, c in enumerate(s):
        result.append(chr(ord(c) ^ key[i % len(key)]))
    return ''.join(result)

# Essayons XOR avec "csaw" comme clé
print(f"XOR avec 'csaw': {xor_with_key(decoded, 'csaw')}")
print(f"XOR avec 'flag': {xor_with_key(decoded, 'flag')}")
print(f"XOR avec 'test': {xor_with_key(decoded, 'test')}")