# Peut-être que @, 0, 3 sont des lettres chiffrées avec un décalage
# ou peut-être que c'est un chiffrement affine ou autre

# Regardons les positions de @ dans le message chiffré:
# esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Positions: 9, 12 (0-indexé)

# Et dans le message décodé Vigenère, @ reste @ car c'est non-alpha

# Peut-être que le message original (avant Vigenère) avait des lettres à la place de @
# et que ces lettres ont été chiffrées en @ ?

# Essayons de deviner ce que @ pourrait être
# Si @ est une lettre, disons 'a', alors dans le chiffrement Vigenère:
# @ (non-alpha) reste @, donc ce n'est pas ça.

# Peut-être que le message chiffré original a été créé en prenant un message en clair
# et en appliquant Vigenère, puis en remplaçant certaines lettres par des symboles ?

# Ou peut-être que c'est un chiffrement de substitution simple où:
# e->c, s->a, n->s, p->w, etc.

# Essayons de trouver le mapping complet en comparant le cipher et le plain attendu
# Si le plain attendu est "csaw{...}" et le cipher est "esnp{...}"

# On sait que:
# e -> c
# s -> a
# n -> s
# p -> w

# Pour le reste, on ne connaît pas le plain. Mais on peut essayer de deviner
# en regardant les patterns de mots.

# Le message décodé partiel est: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}
# Si on suppose que 0=o, 3=e, alors:
# csaw{boc_@lg@el_zuoh_pzege_eo_ooof}

# Essayons de trouver des mots anglais qui correspondent:
# boc -> doc ? (b->d, donc décalage +2)
# @lg@el -> ?lg?el
# zuoh -> ?uoh ou ?oo?
# pzege -> ?e?e?
# eo -> ?o
# ooof -> ?oo?

# Peut-être que le message est: csaw{doc_for_all_time_is_best}
# Vérifions:
# doc -> b0c (d->b, o->0, c->c)
# for -> @lg@el ? Non, for a 3 lettres, @lg@el a 6 caractères.

# Attends, regardons la structure:
# csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}
# word1_word2_word3_word4_word5_word6

# word1: b0c (3 chars)
# word2: @lg@el (6 chars)
# word3: zu0h (4 chars)
# word4: pz3g3 (5 chars)
# word5: e0 (2 chars)
# word6: o00f (4 chars)

# Peut-être que c'est: csaw{the_quick_brown_fox_jumps_over}
# the (3) -> b0c ?
# quick (5) -> @lg@el (6) ? Non.

# Essayons autre chose: csaw{find_the_flag_in_the_video}
# find (4) -> b0c (3) ? Non.

# Peut-être que c'est un message en français ?
# csaw{le_mot_caché_dans_la_vidéo}