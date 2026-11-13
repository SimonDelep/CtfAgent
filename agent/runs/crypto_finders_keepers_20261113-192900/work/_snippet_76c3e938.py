import base64

# Chaîne Base64 extraite
b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Chiffrement Vigenère - fonction de déchiffrement
def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            # Déterminer si majuscule ou minuscule
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            # Déchiffrer
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            # Caractères non alphabétiques restent tels quels
            result.append(char)
    return ''.join(result)

# Clé déduite précédemment
key = "cantfind"
decrypted = vigenere_decrypt(decoded, key)
print(f"Déchiffré avec clé '{key}': {decrypted}")

# Vérifions aussi avec la clé 'cant' seule
key2 = "cant"
decrypted2 = vigenere_decrypt(decoded, key2)
print(f"Déchiffré avec clé '{key2}': {decrypted2}")
