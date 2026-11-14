# Ciphertext: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Plaintext supposé: csaw{you_always_know_where_to_look}

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
plaintext = "csaw{you_always_know_where_to_look}"

# Trouver la clé Vigenère nécessaire
def find_key(ciphertext, plaintext):
    key = []
    ct_idx = 0
    for i, p_char in enumerate(plaintext):
        if p_char.isalpha():
            c_char = ciphertext[ct_idx]
            base = ord('A') if c_char.isupper() else ord('a')
            p_base = ord('A') if p_char.isupper() else ord('a')
            shift = (ord(c_char) - base - (ord(p_char) - p_base)) % 26
            key.append(chr(shift + ord('a')))
            ct_idx += 1
        else:
            key.append(p_char)  # Les non-lettres restent tels quels
    return ''.join(key)

key = find_key(ciphertext, plaintext)
print("Clé nécessaire:", key)

# Vérifions avec cette clé
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_idx % len(key)]
            if key_char.isalpha():
                key_shift = ord(key_char.lower()) - ord('a')
            else:
                key_shift = 0
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

print("Décryptage avec cette clé:", vigenere_decrypt(ciphertext, key))