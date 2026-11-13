# Analysons le caractère '{' dans le brut
# '{' a pour code ASCII 123
# Si on XOR 123 avec la clé, on devrait obtenir '{' pour que le résultat soit correct
# Mais on obtient '}' (125)

# Donc 123 XOR k = 125 => k = 123 XOR 125 = 6
# La clé à la position 4 (après les 4 lettres du préfixe) est 6

# Vérifions la séquence de la clé :
# Position 0: e XOR c = 6
# Position 1: s XOR s = 0
# Position 2: n XOR a = 15
# Position 3: p XOR w = 7
# Position 4: { XOR { = 0 (si on veut garder '{')

# Mais on obtient '}' qui est 125, et '{' est 123
# 123 XOR 6 = 125 = '}'
# Donc la clé à la position 4 est 6, ce qui correspond à key[4 % 4] = key[0] = 6

# C'est cohérent ! La clé est bien [6, 0, 15, 7] et elle s'applique cycliquement.

# Le problème est que le résultat donne "csaw}" au lieu de "csaw{"
# Attends, regardons de plus près :
brut = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7]

# Position 0: 'e' XOR 6 = 'c'
# Position 1: 's' XOR 0 = 's'
# Position 2: 'n' XOR 15 = 'a'
# Position 3: 'p' XOR 7 = 'w'
# Position 4: '{' XOR 6 = '}' (car 123 XOR 6 = 125)

# Donc le résultat est "csaw}"... mais on veut "csaw{"
# Peut-être que le flag original n'a pas d'accroche, ou que le format est différent ?

# Ou peut-être que le message chiffré est juste le contenu sans les accolades ?
# Le flag attendu est csaw{...}, donc peut-être qu'on doit ajouter les accolades ?

# Mais regardons le contenu déchiffré :
result = xor_decrypt(brut, key)
print("Résultat:", result)

# Le résultat commence par "csaw}" ce qui est étrange
# Peut-être que le message original avait "csaw{" et a été chiffré avec une clé différente ?

# Autre possibilité : peut-être que le XOR ne s'applique qu'au contenu entre les accolades ?
# Le préfixe "esnp" est chiffré en "csaw", et le contenu "{...}" est chiffré séparément ?

# Essayons de déchiffrer seulement le contenu entre les accolades
content = brut[4:]  # "{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("\nContenu brut:", content)

# Si on XOR le contenu avec la clé en commençant à la position 0 :
content_decrypted = xor_decrypt(content, key)
print("Contenu déchiffré:", content_decrypted)

# Ou peut-être qu'il faut continuer la clé à partir de la position 4 ?
# La clé est cyclique, donc position 4 correspond à key[0] = 6
# C'est ce qu'on a déjà fait.

# Autre idée : peut-être que le message original est "csaw{...}" et qu'il a été chiffré
# en "esnp{...}" avec une clé qui fait e->c, s->s, n->a, p->w
# Et le contenu entre accolades est aussi chiffré avec la même clé ?

# Dans ce cas, le résultat "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr" serait le flag déchiffré
# Mais il commence par "csaw}" au lieu de "csaw{"

# Peut-être que le "}" est correct et que le flag est csaw}...{...} ?
# Ou peut-être qu'il y a une erreur dans l'interprétation ?

# Regardons les caractères spéciaux dans le résultat
print("\nAnalyse des caractères:")
for i, c in enumerate(result):
    print(f"Position {i}: '{c}' (ord={ord(c)})")