def xor_decrypt(ciphertext, key):
    result = []
    for i, c in enumerate(ciphertext):
        k = key[i % len(key)]
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

key = [6, 0, 15, 7]
brut = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

result = xor_decrypt(brut, key)
print("Résultat complet:", result)

# Le résultat est "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
# Le premier caractère après "csaw" est '}' au lieu de '{'
# Peut-être que le flag est juste ce résultat, ou qu'il faut le formater différemment

# Essayons de voir si le contenu ressemble à quelque chose de lisible
# Peut-être que le XOR n'est pas la bonne approche, ou qu'il y a une autre couche

# Regardons si le résultat contient des mots lisibles
print("\nAnalyse du résultat:")
print(result)

# Peut-être que le message original est en anglais et que le XOR a été appliqué
# Essayons de voir si on peut identifier des mots
# "csaw" est le préfixe, donc le reste devrait être le contenu du flag

# Le contenu est "}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
# Ça ne ressemble pas à du texte lisible...

# Peut-être que le XOR n'est pas la bonne clé, ou qu'il y a une autre couche de chiffrement ?

# Autre idée : peut-être que le message chiffré est "esnp{...}" et que le message original est "csaw{...}"
# Mais le contenu entre accolades est aussi chiffré avec une clé différente ?

# Essayons de déchiffrer seulement le contenu entre les accolades avec une clé différente
content = brut[5:-1]  # "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" (sans les accolades)
print("\nContenu entre accolades:", content)

# Si on XOR le contenu avec la clé [6, 0, 15, 7] en commençant à la position 0 :
content_decrypted = xor_decrypt(content, key)
print("Contenu déchiffré:", content_decrypted)

# Ou peut-être qu'il faut continuer la clé à partir de la position 4 (après "esnp") ?
# La clé est cyclique, donc position 0 du contenu correspond à position 5 du message original
# Position 5 % 4 = 1, donc key[1] = 0
content_decrypted2 = []
for i, c in enumerate(content):
    k = key[(i + 5) % 4]  # Continuer la clé à partir de la position 5
    content_decrypted2.append(chr(ord(c) ^ k))
print("Contenu déchiffré (clé continue):", ''.join(content_decrypted2))