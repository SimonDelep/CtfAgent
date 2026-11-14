# Let's try to understand "jc" better
# j = 9 (0-indexed), c = 2 (0-indexed)
# Maybe we need to apply a Vigenère with key "jc" to the plaintext?

plaintext_content = "y0u_@lw@ys_kn0w_wh3r3_t0_l00k"

def vigenere_encrypt(text, key):
    result = []
    k_idx = 0
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = ord(key[k_idx % len(key)].lower()) - ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
            k_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Encrypt the plaintext content with "jc"
encrypted_with_jc = vigenere_encrypt(plaintext_content, "jc")
print(f"Plaintext encrypted with 'jc': {encrypted_with_jc}")

# What if we need to decrypt the ciphertext with a different key?
# Let's try to find a key that gives a different plaintext

ciphertext_content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# What if the key is "finders" or "keepers"?
def vigenere_decrypt(text, key):
    result = []
    k_idx = 0
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = ord(key[k_idx % len(key)].lower()) - ord('a')
            result.append(chr((ord(c) - base - shift) % 26 + base))
            k_idx += 1
        else:
            result.append(c)
    return ''.join(result)

print(f"With 'finders': {vigenere_decrypt(ciphertext_content, 'finders')}")
print(f"With 'keepers': {vigenere_decrypt(ciphertext_content, 'keepers')}")

# What if the key is "canva"?
print(f"With 'canva': {vigenere_decrypt(ciphertext_content, 'canva')}")

# What if the key is "engine"?
print(f"With 'engine': {vigenere_decrypt(ciphertext_content, 'engine')}")

# What if the key is "creator"?
print(f"With 'creator': {vigenere_decrypt(ciphertext_content, 'creator')}")