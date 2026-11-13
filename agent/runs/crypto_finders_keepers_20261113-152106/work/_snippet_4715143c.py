import base64

# Le texte Base64 décodé
encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
ciphertext = base64.b64decode(encoded).decode('utf-8')
print(f"Ciphertext: {ciphertext}")

# Clé Vigenère
key = "cantfind"

def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            shift = ord(key[key_idx % len(key)]) - ord('a')
            decrypted = chr((ord(c) - base - shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

decrypted = vigenere_decrypt(ciphertext, key)
print(f"Décrypté avec clé '{key}': {decrypted}")

# Essayons aussi avec la clé 'cant'
key2 = "cant"
decrypted2 = vigenere_decrypt(ciphertext, key2)
print(f"Décrypté avec clé '{key2}': {decrypted2}")