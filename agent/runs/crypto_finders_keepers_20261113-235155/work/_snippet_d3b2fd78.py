# Let's check if "jc" as a key gives something meaningful
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
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

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Try with key "jc"
print("With key 'jc':")
print(vigenere_decrypt(ciphertext, "jc"))

# Try with key "finders"
print("\nWith key 'finders':")
print(vigenere_decrypt(ciphertext, "finders"))

# Try with key "keepers"
print("\nWith key 'keepers':")
print(vigenere_decrypt(ciphertext, "keepers"))

# Try with key "finders_keepers"
print("\nWith key 'finders_keepers':")
print(vigenere_decrypt(ciphertext, "finders_keepers"))

# Maybe the key is derived from "engine=jc" - try "engine"
print("\nWith key 'engine':")
print(vigenere_decrypt(ciphertext, "engine"))

# Try "canva"
print("\nWith key 'canva':")
print(vigenere_decrypt(ciphertext, "canva"))