# Analyser la transformation de "esnp" vers "csaw"
# e -> c : -2 ou XOR 6
# s -> s : 0
# n -> a : -9 ou XOR 15
# p -> w : +7 ou XOR 7

# Peut-être que c'est une substitution simple où chaque lettre est décalée
# e(4) -> c(2) : -2
# s(18) -> s(18) : 0
# n(13) -> a(0) : -13
# p(15) -> w(22) : +7

# Ou peut-être que le pattern est différent. Regardons le payload complet.
# "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Peut-être que c'est une substitution où chaque caractère est décalé d'un certain montant
# basé sur sa position ou une clé

# Essayons de voir si c'est un décalage constant (Caesar)
decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Cherchons le décalage qui transforme "esnp{" en "csaw{"
# e->c = -2, s->s = 0, n->a = -13, p->w = +7, {->{ = 0
# Pas constant

# Peut-être que la clé est basée sur le mot "finderskeepers" ou quelque chose comme ça
# Ou peut-être que c'est une Vigenère

# Essayons de décoder le payload comme si c'était du leetspeak avancé
# d0c -> doc ? @yz -> ayz ? @gl -> agl ?
# mn0j -> mnoj ? pm3z3 -> pmeze ? g0 -> go ? o00s -> ooo s ?

# "doc_ayzagl_mnoj_pmeze_go_ooos" - pas très lisible

# Peut-être que c'est une substitution monoalphabétique complète
# Regardons les fréquences ou essayons de deviner le mot

# Le format est probablement csaw{...} donc cherchons un mot qui correspond au pattern
# d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# ??c_???@??_???_???_??_???

# Peut-être que @ = 'a' et 0 = 'o' et 3 = 'e'
# d0c -> doc
# @yz -> ayz
# @gl -> agl
# mn0j -> mnoj
# pm3z3 -> pmeze
# g0 -> go
# o00s -> ooo s

# "doc_ayzagl_mnoj_pmeze_go_ooos"

# Peut-être que c'est "doc_ayzagl" -> "doc_ayzagl" n'a pas de sens
# Essayons de voir si c'est un anagramme ou quelque chose

# Ou peut-être que le flag est simplement "esnp{...}" et qu'il faut le soumettre tel quel?
# Mais le format est csaw{...}

# Attends, peut-être que "esnp" est "csaw" décodé avec une clé, et le reste aussi
# Mais avec quelle clé?

# Regardons la différence entre les positions:
# e(4) -> c(2) : -2
# s(18) -> s(18) : 0
# n(13) -> a(0) : -13
# p(15) -> w(22) : +7

# -2, 0, -13, +7... pas de pattern évident

# Peut-être que la clé est "finders" ou "keepers"
key_word = "finders"
decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw{"

# Vérifions si key_word XOR avec decoded donne expected_prefix
for i, (d, e) in enumerate(zip(decoded[:5], expected_prefix)):
    k = key_word[i % len(key_word)]
    xor_result = chr(ord(d) ^ ord(k))
    print(f"Position {i}: '{d}' ^ '{k}' = '{xor_result}' (attendu '{e}')")