# Ciphertext: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Décodé du Base64
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Test Vigenère avec clé "jc"
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_idx % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

print("Clé 'jc':", vigenere_decrypt(ciphertext, "jc"))
print("Clé 'jc' (majuscule):", vigenere_decrypt(ciphertext, "JC"))

# Peut-être que jc signifie un décalage spécifique
# j = 9, c = 2 (0-indexed)
# Ou peut-être que c'est un décalage de 10 et 3 (1-indexed)
print("\nDécalage César j=9:", ''.join([chr((ord(c) - ord('a') - 9) % 26 + ord('a')) if c.islower() else c for c in ciphertext]))