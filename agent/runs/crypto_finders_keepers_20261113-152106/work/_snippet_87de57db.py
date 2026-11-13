import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="

# Décode Base64
decoded = base64.b64decode(encoded)
print(f"Bytes: {decoded}")
print(f"String: {decoded.decode('utf-8')}")

# Peut-être que c'est XOR avec une clé
# Si le flag commence par "csaw{", alors:
# e ^ key = c => key = e ^ c = 101 ^ 99 = 2
# s ^ key = s => key = s ^ s = 0
# n ^ key = a => key = n ^ a = 110 ^ 97 = 13
# p ^ key = w => key = p ^ w = 112 ^ 119 = 7

# Les clés ne sont pas constantes. Peut-être une clé répétitive?
# e ^ c = 2, s ^ s = 0, n ^ a = 13, p ^ w = 7
# Clé potentielle: [2, 0, 13, 7, ...]

# Essayons de décoder avec XOR en supposant que le plaintext est "csaw{..."
ciphertext = decoded
plaintext_guess = b"csaw{"
key = [c ^ p for c, p in zip(ciphertext[:5], plaintext_guess)]
print(f"Clé déduite: {key}")

# Appliquons cette clé répétitivement
key_extended = (key * 10)[:len(ciphertext)]
result = bytes([c ^ k for c, k in zip(ciphertext, key_extended)])
print(f"Résultat XOR: {result}")

# Peut-être que la clé est "csaw" ou quelque chose comme ça
for test_key in [b"csaw", b"flag", b"key", b"secret", b"finders"]:
    key_ext = (test_key * (len(ciphertext) // len(test_key) + 1))[:len(ciphertext)]
    result = bytes([c ^ k for c, k in zip(ciphertext, key_ext)])
    print(f"XOR avec {test_key}: {result}")