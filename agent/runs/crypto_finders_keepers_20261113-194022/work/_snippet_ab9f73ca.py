import base64

# Chaîne Base64 extraite
b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Fonction Vigenère déchiffrement
def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.lower()
    key_len = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('a')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)

# Tester avec la clé 'cantfindit'
key = "cantfindit"
decrypted = vigenere_decrypt(decoded, key)
print(f"Déchiffré avec '{key}': {decrypted}")

# Tester avec 'cantfind'
key2 = "cantfind"
decrypted2 = vigenere_decrypt(decoded, key2)
print(f"Déchiffré avec '{key2}': {decrypted2}")

# Tester avec 'cant'
key3 = "cant"
decrypted3 = vigenere_decrypt(decoded, key3)
print(f"Déchiffré avec '{key3}': {decrypted3}")