import base64

# Le texte Base64 décodé
encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Maintenant, appliquons la clé Vigenère "cantfind"
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

decrypted = vigenere_decrypt(decoded, key)
print(f"Décrypté avec clé '{key}': {decrypted}")

# Maintenant, appliquons la substitution Leet
text = decrypted
leet_map = {
    '0': 'o',
    '@': 'a',
    '3': 'e',
    '1': 'i',
    '5': 's',
    '7': 't',
    '4': 'a',
    '2': 'z',
    '8': 'b',
    '9': 'g',
    '6': 'g',
}

result = []
for c in text:
    if c in leet_map:
        result.append(leet_map[c])
    else:
        result.append(c)

leet_decoded = ''.join(result)
print(f"Après substitution Leet: {leet_decoded}")

# Peut-être que le flag est le texte déchiffré avec Vigenère, sans substitution Leet
# Ou peut-être que le flag est le texte après substitution Leet

# Essayons de voir si le texte déchiffré avec Vigenère est le bon flag
print(f"Flag candidat 1 (Vigenère seul): {decrypted}")
print(f"Flag candidat 2 (Leet seul): {leet_decoded}")