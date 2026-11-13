def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            key_char = key[key_index % len(key)]
            shift = ord(key_char.lower()) - ord('a')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayons différentes clés
keys_to_try = ["cantfind", "cant", "find", "finders", "keepers", "cantfindme", "cantfindit", "cantfindyou", "finderskeepers"]

for key in keys_to_try:
    decrypted = vigenere_decrypt(ciphertext, key)
    print(f"Clé '{key}': {decrypted}")