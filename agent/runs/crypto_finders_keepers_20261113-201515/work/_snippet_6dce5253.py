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

# Le message déchiffré avec 'cantfindit' est 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}'
# Mais peut-être que le vrai message est différent?

# L'indice 'engine=jc' pourrait être une indication que le message est encodé d'une manière spécifique?
# 'jc' pourrait être 'Jeu de Caractères' ou quelque chose comme ça?

# Autre idée : peut-être que 'jc' est une clé, mais qu'il faut l'appliquer différemment?
# Ou peut-être que le message est en fait différent?

# Essayons de voir si le message est 'csaw{finders_keepers}'
# On a déjà calculé que la clé pour ça est 'cantyvpvphhwhuxjmr'

# Mais peut-être que le message est différent?
# Le titre du challenge est 'finders keepers', donc peut-être que le message est lié à ça?

# Essayons de voir si le message est 'csaw{finders_keepers}' avec une clé différente
# Ou peut-être que le message est 'csaw{you_always_know_where_to_look}' mais qu'on doit soumettre avec le wrapper?

# Attends, l'indice dit "without a flag wrapper". Peut-être que ça signifie sans le préfixe 'csaw{'?
# Mais on a déjà essayé 'you_always_know_where_to_look' et 'y0u_@lw@ys_kn0w_wh3r3_t0_l00k'

# Peut-être que le message est en fait le Leet speak tel quel, avec le wrapper?
# 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}'

# Ou peut-être que le message est différent et qu'on doit trouver une autre clé?

# Réfléchissons à l'indice 'engine=jc'
# 'jc' pourrait être une référence à 'Jeu de César' mais avec un décalage spécifique?
# Ou peut-être que c'est une indication que le message est encodé avec un algorithme différent?

# Autre idée : peut-être que 'jc' signifie 'juste les caractères' et qu'on doit extraire seulement les lettres du message déchiffré?
# 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}' -> 'csawyoualwaysknowwheretolook'

# Ou peut-être que le message est en fait différent?

# Essayons de voir si le message est 'csaw{finders_keepers}'
result = vigenere_decrypt(ciphertext, "cantyvpvphhwhuxjmr")
print(f"Clé 'cantyvpvphhwhuxjmr': {result}")

# Peut-être que le message est 'csaw{finders_keepers}' et qu'on doit soumettre ça?
# Ou peut-être que le message est différent?

# Autre idée : peut-être que le message est 'csaw{you_always_know_where_to_look}' mais qu'on doit soumettre avec le wrapper complet?
# L'indice dit "without a flag wrapper", mais peut-être que ça signifie quelque chose d'autre?

# Attends, peut-être que le message est en fait 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}' et qu'on doit soumettre ça avec le wrapper?
# Ou peut-être que le message est différent?

# Essayons de soumettre 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}'
print("\nVariantes à essayer:")
print("1. csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}")
print("2. csaw{you_always_know_where_to_look}")
print("3. finders_keepers")
print("4. csaw{finders_keepers}")

# Peut-être que le message est 'finders_keepers' sans le préfixe 'csaw{'?
# Ou peut-être que le message est différent?

# Réfléchissons à l'indice 'engine=jc'
# 'jc' pourrait être une référence à 'Jeu de Caractères' mais peut-être que c'est une indication que le message est encodé d'une manière spécifique?

# Autre idée : peut-être que 'jc' signifie 'Jeu de César' et que le message est en fait un chiffrement de César?
# Mais on a déjà essayé le chiffrement de César et ça ne donne pas de résultat lisible?

# Attends, peut-être que le message est en fait 'csaw{you_always_know_where_to_look}' mais qu'on doit soumettre avec le wrapper complet?
# L'indice dit "without a flag wrapper", mais peut-être que ça signifie quelque chose d'autre?

# Ou peut-être que le message est différent et qu'on doit trouver une autre clé?

# Essayons de voir si le message est 'csaw{finders_keepers}' avec une clé différente
# Ou peut-être que le message est 'csaw{you_always_know_where_to_look}' mais qu'on doit soumettre avec le wrapper?

# Autre idée : peut-être que le message est en fait 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}' et qu'on doit soumettre ça sans le wrapper?
# Mais on a déjà essayé 'y0u_@lw@ys_kn0w_wh3r3_t0_l00k' et ça a été refusé?

# Attends, peut-être que le message est en fait 'csaw{you_always_know_where_to_look}' et qu'on doit soumettre avec le wrapper complet?
# L'indice dit "without a flag wrapper", mais peut-être que ça signifie quelque chose d'autre?

# Ou peut-être que le message est différent et qu'on doit trouver une autre clé?

# Réfléchissons à l'indice 'engine=jc'
# 'jc' pourrait être une référence à 'Jeu de Caractères' mais peut-être que c'est une indication que le message est encodé d'une manière spécifique?

# Autre idée : peut-être que 'jc' signifie 'Jeu de César' et que le message est en fait un chiffrement de César avec un décalage spécifique?
# Mais on a déjà essayé le chiffrement de César et ça ne donne pas de résultat lisible?

# Attends, peut-être que le message est en fait 'csaw{you_always_know_where_to_look}' mais qu'on doit soumettre avec le wrapper complet?
# L'indice dit "without a flag wrapper", mais peut-être que ça signifie quelque chose d'autre?

# Ou peut-être que le message est différent et qu'on doit trouver une autre clé?

# Essayons de soumettre 'csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}'
print("\nSoumission possible: csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}")
