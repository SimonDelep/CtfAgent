# Nettoyer le Leet speak du message déchiffré
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfindit"

def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

plaintext_leet = vigenere_decrypt(ciphertext, key)
print(f"Plaintext Leet: {plaintext_leet}")

# Nettoyer le Leet speak
leet_map = {
    '0': 'o',
    '@': 'a',
    '3': 'e',
    '1': 'i',
    '4': 'a',
    '7': 't',
    '5': 's',
    '9': 'g',
    '6': 'g',
    '8': 'b',
    '2': 'z',
}

def clean_leet(text):
    result = []
    for char in text:
        if char in leet_map:
            result.append(leet_map[char])
        else:
            result.append(char)
    return ''.join(result)

cleaned = clean_leet(plaintext_leet)
print(f"Cleaned: {cleaned}")

# Extraire le contenu sans accolades
if cleaned.startswith("csaw{") and cleaned.endswith("}"):
    content = cleaned[5:-1]
    print(f"Content: {content}")