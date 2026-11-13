# Payload original après Base64 : esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On sait que esnp -> csaw

# Peut-être que c'est une substitution où chaque lettre est décalée d'un montant constant
# par rapport à sa position dans l'alphabet, mais avec un décalage différent pour chaque lettre.

# En fait, regardons la différence entre les lettres dans le préfixe :
# e(4) -> c(2) : -2
# s(18) -> s(18) : 0
# n(13) -> a(0) : -13
# p(15) -> w(22) : +7

# Ce n'est pas constant. Peut-être que c'est une substitution arbitraire.

# Mais attendons, peut-être que c'est un décalage basé sur la position de la lettre dans le mot.
# e est à la position 0, s à la position 1, n à la position 2, p à la position 3.
# e(4) -> c(2) : -2 = 0 - 2 ?
# s(18) -> s(18) : 0 = 1 - 1 ?
# n(13) -> a(0) : -13 = 2 - 15 ?
# p(15) -> w(22) : +7 = 3 + 4 ?

# Non, ça ne semble pas être un pattern simple.

# Essayons une autre approche : peut-être que le flag est "csaw{doc_azure_gl_maj_wmez_go_ooos}"
# et que je dois juste deviner.

# En fait, regardons le payload décodé partiellement : csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}
# Si on remplace 0->o, 3->e, @->_ :
# csaw{doc_yz_gl_maoj_wmeze_go_ooos}

# "yz_gl_maoj_wmeze_go_ooos"
# Peut-être que c'est "azure_gl_maj_wmez_go_ooos" ?

# Regardons "yz" : si y->a et z->z, alors "yz" -> "az"
# "gl" : si g->u et l->r, alors "gl" -> "ur" ? Non, "azure" a "ur" après "az".

# Attends, "azure" est a-z-u-r-e. Donc "az" + "ure".
# Si "yz" -> "az", alors y->a, z->z.
# Et "gl" -> "ure" ? g->u, l->r, et il manque le 'e'.

# Hmm, peut-être que c'est "az_gl" et que "gl" est correct.

# En fait, peut-être que le flag est "csaw{doc_azure_gl_maj_wmez_go_ooos}"
# et que la substitution est :
# y->a, z->z, g->u, l->r, a->e, j->_, m->m, a->a, o->i, j->n, w->w, m->e, e->e, z->z, e->e

# C'est trop compliqué. Essayons de voir si c'est un ROT13 sur les lettres seulement.

payload = "csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}"

# Appliquer ROT13 seulement sur les lettres
def rot13_on_letters(s):
    result = []
    for c in s:
        if c.isalpha():
            if c.islower():
                result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

rot13_payload = rot13_on_letters(payload)
print(f"ROT13 sur les lettres : {rot13_payload}")

# Essayons aussi ROT-13 (qui est la même chose)
# Et essayons d'autres décalages
for shift in range(1, 26):
    def shift_on_letters(s, shift):
        result = []
        for c in s:
            if c.isalpha():
                if c.islower():
                    result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(c)
        return ''.join(result)
    
    shifted = shift_on_letters(payload, shift)
    # Vérifier si le résultat contient des mots anglais plausibles
    if 'doc' in shifted.lower() or 'the' in shifted.lower() or 'and' in shifted.lower():
        print(f"Shift {shift}: {shifted}")