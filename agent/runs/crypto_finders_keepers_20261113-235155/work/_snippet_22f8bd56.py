def vigenere_decrypt_custom(ciphertext, key_values):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_shift = key_values[key_index % len(key_values)]
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Clé jc : j=9, c=2 (0-indexed: a=0, b=1, ..., j=9, c=2)
key_values = [9, 2]
print(f"Clé [9,2]: {vigenere_decrypt_custom(ciphertext, key_values)}")

# Clé jc : j=10, c=3 (1-indexed)
key_values = [10, 3]
print(f"Clé [10,3]: {vigenere_decrypt_custom(ciphertext, key_values)}")

# Clé jc : j=9, c=2 mais en sens inverse (chiffrement au lieu de déchiffrement)
def vigenere_encrypt_custom(ciphertext, key_values):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_shift = key_values[key_index % len(key_values)]
            encrypted = chr((ord(char) - base + key_shift) % 26 + base)
            result.append(encrypted)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

print(f"Chiffrement avec [9,2]: {vigenere_encrypt_custom(ciphertext, key_values)}")