# Recalculons correctement
# cipher = "esnp", plain = "csaw"
# key = (cipher - plain) mod 26

cipher = "esnp"
plain_expected = "csaw"

print("Calcul de la clé:")
for i, (c, p) in enumerate(zip(cipher, plain_expected)):
    c_val = ord(c.lower()) - ord('a')
    p_val = ord(p.lower()) - ord('a')
    k_val = (c_val - p_val) % 26
    print(f"  {c} ({c_val}) -> {p} ({p_val}): key = {k_val} = '{chr(k_val + ord('a'))}'")

# Donc la clé est "cant"
# Maintenant décodons tout le message avec la clé "cant"

def vigenere_decrypt_full(cipher_text, key):
    result = []
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            cipher_val = ord(char) - base
            key_val = ord(key[key_index % len(key)].lower()) - ord('a')
            plain_val = (cipher_val - key_val) % 26
            result.append(chr(plain_val + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

cipher_full = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("\nDécodage avec clé 'cant':")
print(vigenere_decrypt_full(cipher_full, "cant"))