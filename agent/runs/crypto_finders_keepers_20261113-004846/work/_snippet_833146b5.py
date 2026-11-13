# La chaîne chiffrée
cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Le préfixe attendu
plain_prefix = "csaw{"

# Trouver la clé XOR en XORant le début
key = []
for i in range(len(plain_prefix)):
    key.append(ord(cipher[i]) ^ ord(plain_prefix[i]))

print("Clé XOR déduite du préfixe:", key)
print("Clé XOR en hex:", [hex(k) for k in key])

# Essayer d'appliquer cette clé répétée sur toute la chaîne
def xor_with_key_repeat(cipher_text, key):
    result = []
    for i, c in enumerate(cipher_text):
        result.append(chr(ord(c) ^ key[i % len(key)]))
    return ''.join(result)

# Clé de longueur 5 (csaw{)
key5 = [ord(cipher[i]) ^ ord(plain_prefix[i]) for i in range(5)]
print("\nAvec clé de longueur 5:", xor_with_key_repeat(cipher, key5))

# Clé de longueur 4 (csaw)
key4 = [ord(cipher[i]) ^ ord(plain_prefix[i]) for i in range(4)]
print("Avec clé de longueur 4:", xor_with_key_repeat(cipher, key4))
