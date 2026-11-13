# Payload original après décodage Base64 : esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On a décodé esnp -> csaw, mais peut-être que d'autres lettres sont aussi substituées

# Regardons le pattern : 
# Original: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On veut: csaw{...}

# Si c'est une substitution monoalphabétique complète, on peut essayer de trouver la clé
# en comparant avec un flag attendu typique.

# Essayons de deviner ce que pourrait être le flag. 
# "doc" semble correct. "ayzagl" pourrait être "azure" ? 
# "maoj" pourrait être "manj" ou "main" ?
# "wmeze" pourrait être "wmez" ou "weeze" ?

# Regardons les lettres dans le payload décodé partiellement :
# csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}

# Si on suppose que c'est une phrase en anglais :
# "doc_ayzagl_maoj_wmeze_go_ooos"

# Peut-être que c'est "doc_azure_main_weeze_go_ooos" ?
# Ou "doc_azure_maj_wmez_go_ooos" ?

# Essayons une autre approche : peut-être que la substitution est un décalage de Caesar
# mais appliqué seulement sur certaines lettres.

# Regardons les lettres dans le payload original (après Base64) :
original = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Les lettres sont : e, s, n, p, d, c, y, z, g, l, m, n, j, p, m, z, g, o, s

# Si on compare avec ce qu'on attend (csaw{...}), on a :
# e -> c
# s -> s (inchangé)
# n -> a
# p -> w

# Peut-être que c'est une substitution basée sur un décalage variable ?
# Ou peut-être que c'est un chiffrement de Vigenère ?

# Essayons de voir si c'est un décalage constant sur les lettres :
# e(4) -> c(2) : -2
# s(18) -> s(18) : 0
# n(13) -> a(0) : -13
# p(15) -> w(22) : +7

# Ce n'est pas constant. Peut-être que c'est une substitution arbitraire.

# Regardons le contenu décodé avec leet : doc_ayzagl_maoj_wmeze_go_ooos
# "ayzagl" -> 6 lettres. "azure" -> 5 lettres. "azgl" -> 4 lettres.
# Peut-être que c'est "doc_azure_gl_maoj_wmeze_go_ooos" ?

# Attends, regardons "ayzagl" : si on enlève le 'y', on a "azagl" qui ressemble à "azagl"
# Ou peut-être que c'est "doc_azure_gl_maj_wmez_go_ooos" ?

# Essayons de voir si c'est "doc_azure_gl_maj_wmez_go_ooos"
# Comparons avec "doc_ayzagl_maoj_wmeze_go_ooos"

# "ayzagl" vs "azure_gl" : a-y-z-a-g-l vs a-z-u-r-e-_-g-l
# C'est différent.

# Peut-être que c'est "doc_azure_gl_main_weeze_go_ooos" ?
# "maoj" -> "main" ? m-a-o-j vs m-a-i-n : o->i, j->n
# "wmeze" -> "weeze" ? w-m-e-z-e vs w-e-e-z-e : m->e, z->z, e->e

# Hmm, c'est compliqué. Essayons une autre approche :
# Peut-être que le flag est "csaw{doc_azure_gl_maj_wmez_go_ooos}" ou quelque chose comme ça.

# Regardons les lettres uniques dans le payload décodé partiellement :
payload = "csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}"
letters = set(c for c in payload if c.isalpha())
print(f"Lettres uniques : {letters}")

# Peut-être que c'est une substitution où chaque lettre est remplacée par une autre
# de manière arbitraire. On a déjà : e->c, s->s, n->a, p->w

# Regardons les autres lettres dans le payload :
# d, c, y, z, g, l, m, j, o
# Et dans le préfixe : e, s, n, p

# Si on suppose que le flag est quelque chose comme "csaw{doc_azure_gl_maj_wmez_go_ooos}"
# Alors on aurait :
# d->d, c->c, y->u, z->r, g->e, l->_, m->m, j->i, o->n, etc.

# Attends, regardons "ayzagl" : si c'est "azure", alors :
# a->a, y->z, z->u, a->r, g->e, l->_ ?
# Non, ça ne correspond pas.

# Peut-être que c'est "doc_azure_gl_maj_wmez_go_ooos" et que la substitution est :
# y->z, z->u, a->r, g->e, l->_, m->m, a->a, o->i, j->n, w->w, m->e, e->e, z->z, e->e

# C'est trop compliqué. Essayons de voir si c'est un ROT sur les lettres seulement.
# Enleçons les chiffres et caractères spéciaux, et appliquons un ROT.

import string

inner = "d0c_@yz@gl_ma0j_wm3z3_g0_o00s"
# Extraire les lettres
letters_only = [c for c in inner if c.isalpha()]
print(f"Lettres dans inner : {''.join(letters_only)}")

# Appliquer ROT13
rot13_letters = [chr((ord(c) - ord('a') + 13) % 26 + ord('a')) if c.islower() else c for c in letters_only]
print(f"ROT13 des lettres : {''.join(rot13_letters)}")

# Peut-être que c'est un décalage de -2 sur les lettres ?
shift_minus_2 = [chr((ord(c) - ord('a') - 2) % 26 + ord('a')) if c.islower() else c for c in letters_only]
print(f"Shift -2 des lettres : {''.join(shift_minus_2)}")

# Shift +2
shift_plus_2 = [chr((ord(c) - ord('a') + 2) % 26 + ord('a')) if c.islower() else c for c in letters_only]
print(f"Shift +2 des lettres : {''.join(shift_plus_2)}")