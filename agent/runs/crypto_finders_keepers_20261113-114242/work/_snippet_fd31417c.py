# Le message chiffré est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Le résultat Vigenère est: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}

# Peut-être que @, 0, 3 sont des substitutions de lettres
# Essayons de deviner le message final

# Pattern: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}
# Si on remplace 0->o, 3->e, @->_
# csaw{bo c_lg_el_zuoh_pzege_eo_ooff}

# Mais ça ne fait pas de sens. Essayons autre chose.

# Peut-être que le message original (avant Vigenère) était déjà en "leet speak"
# et que le Vigenère s'applique seulement aux lettres.

# Regardons si le message décodé a du sens avec des substitutions simples:
decoded = "csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}"

# Substitutions possibles:
# 0 -> o
# 3 -> e
# @ -> ? (peut-être une lettre)

# Essayons 0->o, 3->e
temp = decoded.replace('0', 'o').replace('3', 'e')
print("Avec 0->o, 3->e:", temp)

# Maintenant, que pourrait être @ ?
# Le pattern est: csaw{boc_@lg@el_zuoh_pzege_eo_ooff}
# "boc" pourrait être "doc" ou "bob" ou "boc"
# "@lg@el" - si @ = '_', alors "_lg_el"
# "zuoh" - peut-être "zoo h" ou "zouh"
# "pzege" - peut-être "pege" ou "pzege"
# "eo" - peut-être "to" ou "so"
# "ooff" - peut-être "oofs" ou "oof"

# Essayons @ = '_'
temp2 = temp.replace('@', '_')
print("Avec @->_:", temp2)

# csaw{boc_lg_el_zuoh_pzege_eo_ooff}
# Ça ne semble pas être des mots anglais cohérents.

# Peut-être que la clé Vigenère est différente ?
# Ou peut-être que c'est un autre type de chiffrement.

# Essayons de trouver un mot qui correspond au pattern
# csaw{???_???_???_???_???_???}
# Le format est csaw{word_word_word_word_word_word}

# Regardons les longueurs:
# b0c = 3 lettres
# @lg@el = 6 caractères (2 @ + 4 lettres)
# zu0h = 4 caractères
# pz3g3 = 5 caractères
# e0 = 2 caractères
# o00f = 4 caractères

# Peut-être que c'est: csaw{doc_for_all_time_is_best} ou quelque chose comme ça ?