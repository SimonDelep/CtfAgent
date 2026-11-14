import base64

b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
ciphertext = base64.b64decode(b64).decode('utf-8')
print(f"Ciphertext: {ciphertext}")

# Vigenère standard (seulement les lettres alphabétiques décalées, autres conservés)
def vigenere_decrypt_std(ciphertext, key):
    result = []
    key = key.lower()
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('a')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

# Tester avec 'cant'
print(f"\nAvec 'cant': {vigenere_decrypt_std(ciphertext, 'cant')}")
print(f"Avec 'cantfind': {vigenere_decrypt_std(ciphertext, 'cantfind')}")
print(f"Avec 'cantfindit': {vigenere_decrypt_std(ciphertext, 'cantfindit')}")

# Peut-être que la clé est 'finderskeepers' ou 'finders_keepers' ?
print(f"\nAvec 'finders': {vigenere_decrypt_std(ciphertext, 'finders')}")
print(f"Avec 'keepers': {vigenere_decrypt_std(ciphertext, 'keepers')}")
print(f"Avec 'finderskeepers': {vigenere_decrypt_std(ciphertext, 'finderskeepers')}")
print(f"Avec 'finders_keepers': {vigenere_decrypt_std(ciphertext, 'finders_keepers')}")