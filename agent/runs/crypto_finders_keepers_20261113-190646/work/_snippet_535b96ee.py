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
            # Décalage de la clé
            key_char = key[key_index % len(key)]
            shift = ord(key_char.lower()) - ord('a')
            # Déchiffrer
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfind"
decrypted = vigenere_decrypt(ciphertext, key)
print(f"Ciphertext: {ciphertext}")
print(f"Clé: {key}")
print(f"Déchiffré: {decrypted}")