def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "jc"
print(f"Vigenère avec clé '{key}': {vigenere_decrypt(ciphertext, key)}")

key = "cantfindit"
print(f"Vigenère avec clé '{key}': {vigenere_decrypt(ciphertext, key)}")