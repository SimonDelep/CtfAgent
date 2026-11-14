import base64

# Le ciphertext décodé
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfind"

# Déchiffrer avec Vigenère
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

print("Ciphertext:", ciphertext)
print("Clé:", key)
print("Déchiffré:", vigenere_decrypt(ciphertext, key))

# Vérifions aussi la clé "cant" seule
print("\nAvec clé 'cant':")
print(vigenere_decrypt(ciphertext, "cant"))