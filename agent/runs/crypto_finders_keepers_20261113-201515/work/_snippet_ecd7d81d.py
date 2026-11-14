# Le ciphertext Base64 décodé est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Avec clé 'cantfindit' on obtient: csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}
# Mais les soumissions ont échoué...

# L'indice 'engine=jc' est intéressant. Essayons différentes interprétations:

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Test avec 'jc' comme clé
print("Clé 'jc':", vigenere_decrypt(ciphertext, "jc"))

# Peut-être que 'jc' signifie 'jeu de caractères' ou une variante?
# Essayons 'jc' en majuscule
print("Clé 'JC':", vigenere_decrypt(ciphertext, "JC"))

# Peut-être que c'est 'jc' mais appliqué différemment?
# Ou peut-être que le vrai message est juste le Leet speak nettoyé?

# Nettoyons le message déchiffré avec cantfindit
leet_msg = "csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"
clean_msg = leet_msg.replace('0', 'o').replace('@', 'a').replace('3', 'e').replace('1', 'i').replace('4', 'a').replace('7', 't')
print("Nettoyé:", clean_msg)

# Peut-être que le flag est juste le texte entre accolades?
print("Sans wrapper:", clean_msg[5:-1])
