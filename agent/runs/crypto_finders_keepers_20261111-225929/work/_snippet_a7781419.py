import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Original decoded: {decoded}")

# Peut-être que c'est un XOR avec une clé répétitive
def xor_with_key(s, key):
    result = []
    for i, c in enumerate(s):
        result.append(chr(ord(c) ^ ord(key[i % len(key)])))
    return ''.join(result)

# Essayons XOR avec "csaw" comme clé
print(f"XOR avec 'csaw': {xor_with_key(decoded, 'csaw')}")
print(f"XOR avec 'flag': {xor_with_key(decoded, 'flag')}")
print(f"XOR avec 'test': {xor_with_key(decoded, 'test')}")

# Peut-être que la clé est plus longue ?
# Regardons la structure: esnp{...} devrait être csaw{...}
# Donc les 4 premiers caractères XORés devraient donner "csaw"
# e ^ k1 = c => k1 = e ^ c = 101 ^ 99 = 6
# s ^ k2 = s => k2 = s ^ s = 0
# n ^ k3 = a => k3 = n ^ a = 110 ^ 97 = 15
# p ^ k4 = w => k4 = p ^ w = 112 ^ 119 = 7

key_bytes = [6, 0, 15, 7]
print(f"\nClé XOR déduite: {key_bytes}")

# Appliquons cette clé à tout le message
def xor_with_bytes(s, key_bytes):
    result = []
    for i, c in enumerate(s):
        result.append(chr(ord(c) ^ key_bytes[i % len(key_bytes)]))
    return ''.join(result)

print(f"Message XORé avec clé déduite: {xor_with_bytes(decoded, key_bytes)}")