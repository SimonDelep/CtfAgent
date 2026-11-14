# Vérifions le déchiffrement Vigenère avec la clé 'cantfindit'
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfindit"

def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            # Déterminer si majuscule ou minuscule
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted_char = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

decrypted = vigenere_decrypt(ciphertext, key)
print(f"Ciphertext: {ciphertext}")
print(f"Key: {key}")
print(f"Decrypted: {decrypted}")

# Vérifions aussi avec la clé 'cantfind' (plus courte)
key2 = "cantfind"
decrypted2 = vigenere_decrypt(ciphertext, key2)
print(f"\nWith key '{key2}': {decrypted2}")