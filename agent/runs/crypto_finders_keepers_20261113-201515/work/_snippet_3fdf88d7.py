# Re-vérifions le déchiffrement Vigenère avec la clé cantfindit
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfindit"

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
print(f"Ciphertext: {ciphertext}")
print(f"Key: {key}")
print(f"Plaintext: {plaintext}")
print(f"Length: {len(plaintext)}")

# Vérifions aussi avec d'autres clés potentielles
for test_key in ["cantfind", "finders", "keepers", "finderskeepers", "cantfindit"]:
    pt = vigenere_decrypt(ciphertext, test_key)
    print(f"Key '{test_key}': {pt}")