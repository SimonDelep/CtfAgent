def vigenere_encrypt(text, key):
    result = []
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

def vigenere_decrypt(text, key):
    result = []
    key_idx = 0
    for char in text:
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

plaintext = "csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"

# Appliquer Vigenère avec "jc" sur le plaintext
encrypted_with_jc = vigenere_encrypt(plaintext, "jc")
print(f"Plaintext encrypté avec 'jc': {encrypted_with_jc}")

# Ou peut-être que le ciphertext original doit être decrypté avec une clé différente
# Essayons de trouver quelle clé donnerait "csaw{you_always_know_where_to_look}" (sans Leet)

# Le ciphertext est "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Si le plaintext attendu est "csaw{you_always_know_where_to_look}"
# Alors la clé serait différente

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
target_plaintext = "csaw{you_always_know_where_to_look}"

# Calculer la clé nécessaire
def get_key(ciphertext, plaintext):
    key = []
    c_idx = 0
    p_idx = 0
    while c_idx < len(ciphertext) and p_idx < len(plaintext):
        c_char = ciphertext[c_idx]
        p_char = plaintext[p_idx]
        if c_char.isalpha() and p_char.isalpha():
            c_val = ord(c_char.lower()) - ord('a')
            p_val = ord(p_char.lower()) - ord('a')
            key_val = (c_val - p_val) % 26
            key.append(chr(key_val + ord('a')))
            c_idx += 1
            p_idx += 1
        else:
            c_idx += 1
            p_idx += 1
    return ''.join(key)

key_needed = get_key(ciphertext, target_plaintext)
print(f"Clé nécessaire pour obtenir '{target_plaintext}': {key_needed}")