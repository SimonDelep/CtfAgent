# Peut-être que le préfixe "esnp" est chiffré avec une clé, et le contenu "{...}" avec une autre clé ?
# Ou peut-être que le contenu est chiffré avec la même clé mais en commençant à une position différente ?

# Autre idée : peut-être que le message original est "csaw{...}" et qu'il a été chiffré
# en "esnp{...}" avec une clé qui fait e->c, s->s, n->a, p->w
# Et le contenu entre accolades est chiffré avec la même clé, mais en continuant la séquence ?

# Si le message original est "csaw{content}", alors :
# Position 0: c XOR k0 = e => k0 = 6
# Position 1: s XOR k1 = s => k1 = 0
# Position 2: a XOR k2 = n => k2 = 15
# Position 3: w XOR k3 = p => k3 = 7
# Position 4: { XOR k4 = { => k4 = 0 (si on veut garder '{')

# Mais dans notre cas, le message chiffré a '{' à la position 4, et le résultat a '}'
# Donc k4 = 6 (car 123 XOR 6 = 125)
# Cela signifie que la clé est cyclique : [6, 0, 15, 7, 6, 0, 15, 7, ...]

# Donc le message original devrait avoir un caractère qui XORé avec 6 donne '{' (123)
# Ce caractère est 123 XOR 6 = 125 = '}'
# Donc le message original aurait '}' à la position 4, pas '{'

# Mais le format du flag est csaw{...}, donc le message original devrait avoir '{' à la position 4
# Cela signifie que le message chiffré devrait avoir un caractère qui XORé avec 6 donne '{'
# Ce caractère est 125 = '}'

# Donc si le message chiffré avait '}' à la position 4, le résultat aurait '{'
# Mais le message chiffré a '{' à la position 4, donc le résultat a '}'

# Peut-être que le message original n'a pas d'accroche, et que le format "csaw{...}" est juste pour la soumission ?
# Dans ce cas, le flag serait "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"

# Mais ça semble étrange...

# Autre possibilité : peut-être que le XOR ne s'applique qu'aux caractères alphabétiques ?
# Regardons le message chiffré : "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Les caractères spéciaux sont : {, }, _, @, 0-9

# Si on ne XOR que les lettres, alors :
# e -> c (XOR 6)
# s -> s (XOR 0)
# n -> a (XOR 15)
# p -> w (XOR 7)
# { reste {
# d -> ? (XOR 6) => d (100) XOR 6 = 106 = 'j'... mais on obtient '?' (63)

# Attends, regardons le résultat : "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
# Le 'd' à la position 5 n'a pas été XORé ? Ou il l'a été ?

# Position 5: 'd' (100) XOR key[5%4] = key[1] = 0 => 100 XOR 0 = 100 = 'd'
# Donc 'd' XOR 0 = 'd', c'est correct !

# Position 6: '0' (48) XOR key[6%4] = key[2] = 15 => 48 XOR 15 = 63 = '?'
# Donc '0' XOR 15 = '?', c'est correct !

# Donc le XOR s'applique à tous les caractères, pas seulement aux lettres.

# Le problème est que le résultat commence par "csaw}" au lieu de "csaw{"
# Peut-être que le flag est juste "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr" ?
# Ou peut-être qu'il faut ajouter les accolades autour ?

# Essayons de soumettre le flag tel quel, avec les accolades :
flag = "csaw{" + result[4:] + "}"
print("Flag avec accolades:", flag)

# Ou peut-être que le flag est juste le contenu déchiffré sans les accolades du message chiffré ?
# Le message chiffré est "esnp{...}", donc le contenu entre accolades est "{...}"
# En déchiffrant, on obtient "csaw}..."
# Donc le flag serait "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"

# Mais le format attendu est csaw{...}, donc peut-être qu'il faut remplacer le premier '}' par '{' ?
# Ou peut-être que le message original avait '}' à la position 4, et que le format de soumission ajoute les accolades ?

# Essayons de soumettre le flag tel quel :
print("\nFlag potentiel:", result)
print("Formaté:", "csaw{" + result[4:])