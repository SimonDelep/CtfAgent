# Essayons un chiffrement de Vigenère avec la clé "JC"
# ou peut-être que c'est un décalage basé sur la position

cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si c'est Vigenère avec clé "JC" (J=9, C=2)
# Décryptage: plain = (cipher - key) mod 26

def vigenere_decrypt(cipher_text, key):
    result = []
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            # Convertir en 0-25
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            cipher_val = ord(char) - base
            key_val = ord(key[key_index % len(key)].lower()) - ord('a')
            plain_val = (cipher_val - key_val) % 26
            result.append(chr(plain_val + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

# Essai avec clé "JC"
print("Clé JC:", vigenere_decrypt(cipher, "JC"))

# Essai avec clé "jc"
print("Clé jc:", vigenere_decrypt(cipher, "jc"))

# Essai avec clé "CAESAR"
print("Clé CAESAR:", vigenere_decrypt(cipher, "CAESAR"))

# Essai avec clé "JULES"
print("Clé JULES:", vigenere_decrypt(cipher, "JULES"))