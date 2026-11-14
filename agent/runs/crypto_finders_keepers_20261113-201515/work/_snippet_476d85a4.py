# Essayons avec la clé "jc"
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "jc"

def vigenere_decrypt(ct, k):
    result = []
    key_idx = 0
    for c in ct:
        if c.isalpha():
            shift = ord(k[key_idx % len(k)].lower()) - ord('a')
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

plaintext = vigenere_decrypt(ciphertext, key)
print(f"Clé 'jc': {plaintext}")

# Essayons aussi "engine"
key2 = "engine"
plaintext2 = vigenere_decrypt(ciphertext, key2)
print(f"Clé 'engine': {plaintext2}")

# Et "Canva"
key3 = "Canva"
plaintext3 = vigenere_decrypt(ciphertext, key3)
print(f"Clé 'Canva': {plaintext3}")