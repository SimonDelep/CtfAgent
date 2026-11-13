cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

def xor_decrypt(cipher_text, key_str):
    key = [ord(k) for k in key_str]
    result = []
    for i, c in enumerate(cipher_text):
        result.append(chr(ord(c) ^ key[i % len(key)]))
    return ''.join(result)

# Clé "csaw"
print("Clé 'csaw':", xor_decrypt(cipher, "csaw"))

# Clé "flag"
print("Clé 'flag':", xor_decrypt(cipher, "flag"))

# Clé "secret"
print("Clé 'secret':", xor_decrypt(cipher, "secret"))

# Clé "finders"
print("Clé 'finders':", xor_decrypt(cipher, "finders"))

# Clé "keepers"
print("Clé 'keepers':", xor_decrypt(cipher, "keepers"))

# Clé "hidden"
print("Clé 'hidden':", xor_decrypt(cipher, "hidden"))

# Clé "message"
print("Clé 'message':", xor_decrypt(cipher, "message"))

# Clé "video"
print("Clé 'video':", xor_decrypt(cipher, "video"))

# Clé "mp4"
print("Clé 'mp4':", xor_decrypt(cipher, "mp4"))

# Clé "base64"
print("Clé 'base64':", xor_decrypt(cipher, "base64"))

# Clé "the"
print("Clé 'the':", xor_decrypt(cipher, "the"))

# Clé "a"
print("Clé 'a':", xor_decrypt(cipher, "a"))
