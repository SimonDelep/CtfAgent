import base64

# Ciphertext Base64
b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
ciphertext = base64.b64decode(b64).decode('ascii')
print(f"Ciphertext: {ciphertext}")

# Fonction de déchiffrement Vigenère (lettres seulement, autres chars inchangés)
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            # Déterminer si majuscule ou minuscule
            if c.islower():
                base = ord('a')
            else:
                base = ord('A')
            key_char = key[key_idx % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted_char = chr((ord(c) - base - key_shift) % 26 + base)
            result.append(decrypted_char)
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Clés à tester
keys = ["cantfindit", "cantfind", "finders", "keepers", "finderskeepers", "cant", "find"]

for key in keys:
    decrypted = vigenere_decrypt(ciphertext, key)
    print(f"Clé '{key}': {decrypted}")