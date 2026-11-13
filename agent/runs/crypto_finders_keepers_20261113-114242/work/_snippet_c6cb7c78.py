# Ciphertext avec clé Vigenère "cant"
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cant"

# Décryptage Vigenère (seulement les lettres)
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            # Déterminer si majuscule ou minuscule
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            # Décalage de la clé
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            # Décrypter
            decrypted = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

plaintext = vigenere_decrypt(ciphertext, key)
print(f"Ciphertext: {ciphertext}")
print(f"Clé: {key}")
print(f"Plaintext (après Vigenère): {plaintext}")

# Maintenant appliquer les substitutions de look-alike/leetspeak
# Hypothèses basées sur la structure du flag
substitutions = {
    '0': 'o',  # look-alike
    '3': 'e',  # leetspeak
    '@': '_',  # underscore
}

final = plaintext
for old, new in substitutions.items():
    final = final.replace(old, new)

print(f"Plaintext final (avec substitutions): {final}")