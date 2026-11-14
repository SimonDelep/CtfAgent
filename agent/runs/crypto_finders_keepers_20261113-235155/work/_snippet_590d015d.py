import base64

ciphertext_b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
ciphertext = base64.b64decode(ciphertext_b64).decode('ascii')
print(f"Ciphertext: {ciphertext}")

# Vigenère decryption avec la clé "cantfindit"
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

key = "cantfindit"
plaintext = vigenere_decrypt(ciphertext, key)
print(f"Plaintext avec clé '{key}': {plaintext}")

# Essayons aussi avec "jc" comme clé
plaintext_jc = vigenere_decrypt(ciphertext, "jc")
print(f"Plaintext avec clé 'jc': {plaintext_jc}")

# Essayons de voir si "jc" est une transformation sur la clé
# Peut-être que la clé est "cantfindit" mais avec une transformation "jc"
# Ou peut-être que le ciphertext doit être transformé différemment

# Vérifions la longueur
print(f"Longueur ciphertext: {len(ciphertext)}")
print(f"Longueur plaintext: {len(plaintext)}")