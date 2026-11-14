# Let's verify the Vigenère decryption and check the exact lengths
import base64

ciphertext_b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
ciphertext = base64.b64decode(ciphertext_b64).decode('ascii')
print(f"Ciphertext: {ciphertext}")
print(f"Ciphertext length: {len(ciphertext)}")

# Vigenère decryption with key "cantfindit"
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
print(f"Plaintext (Leet): {plaintext}")
print(f"Plaintext length: {len(plaintext)}")

# Clean version
clean = plaintext.replace('0', 'o').replace('@', 'a').replace('3', 'e')
print(f"Plaintext (clean): {clean}")
print(f"Clean length: {len(clean)}")

# Check character-by-character mapping
print("\nCharacter mapping:")
for i, (c, p) in enumerate(zip(ciphertext, plaintext)):
    if c != p:
        print(f"  {c} -> {p}")