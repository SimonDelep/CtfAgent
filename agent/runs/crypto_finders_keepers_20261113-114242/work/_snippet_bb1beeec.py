# Texte décodé: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On veut obtenir: csaw{...} avec un message lisible

# Si e->c, s->s, n->a, p->w, alors:
# esnp -> csaw

# Maintenant, regardons le reste du message:
# d0c_@yz@gl_mn0j_pm3z3_g0_o00s

# Si on applique la même logique, peut-être que:
# d->?, 0->0, c->?, _->_, @->?, y->?, z->?, g->?, l->?, m->?, n->a, 0->0, j->?, p->w, m->?, 3->3, z->?, 3->3, _->_, g->?, 0->0, _->_, o->?, 0->0, 0->0, s->s

# Attends, regardons plus attentivement. Le message original est:
# esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}

# Si on suppose que c'est une substitution monoalphabétique cohérente,
# alors chaque lettre est remplacée par une autre lettre de manière constante.

# e->c, s->s, n->a, p->w

# Maintenant, pour trouver la substitution complète, on peut essayer de deviner
# le message final en supposant que c'est un message en anglais lisible.

# Le message entre accolades est: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Si on remplace @ par _, on obtient: d0c__yz_gl_mn0j_pm3z3_g0_o00s

# Essayons de voir si c'est un message comme "doc_xyz_gl_mn0j_pm3z3_g0_o00s"
# ou quelque chose comme ça

# En fait, je remarque que le message contient des chiffres et des underscores
# qui pourraient faire partie du message.

# Peut-être que le message est déjà correct et qu'il faut juste appliquer
# la substitution e->c, s->s, n->a, p->w

# Mais alors, que deviennent les autres lettres?

# Essayons de voir si c'est une substitution où chaque lettre est décalée
# d'une valeur fixe, mais avec une exception pour certaines lettres

# Ou peut-être que c'est une substitution de type "keyed cipher"
# où l'alphabet est mélangé selon une clé

# Pour l'instant, essayons de voir si le message a du sens avec une substitution
# où e->c, s->s, n->a, p->w, et les autres lettres restent inchangées

text = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Substitution: e->c, s->s, n->a, p->w
sub_map = {'e': 'c', 's': 's', 'n': 'a', 'p': 'w'}

result = ""
for c in text:
    if c in sub_map:
        result += sub_map[c]
    else:
        result += c

print(f"Résultat avec substitution partielle: {result}")

# Maintenant, essayons de voir si le message a du sens
# en remplaçant @ par _
result2 = result.replace('@', '_')
print(f"Avec @ -> _: {result2}")

# Le résultat est: csaw{d0c__yz_gl_ma0j_wm3z3_g0_o00s}
# Cela ne semble pas très lisible

# Peut-être que la substitution est plus complexe
# et que d'autres lettres sont aussi substituées

# Essayons de voir si c'est une substitution où chaque lettre est décalée
# d'une valeur qui dépend de sa position dans l'alphabet

# Ou peut-être que c'est une substitution de type "affine cipher"
# où chaque lettre est transformée par une fonction affine

# Pour l'instant, essayons de soumettre le flag avec le message actuel
# et voir si c'est correct

print()
print("Flag potentiel:")
print(f"csaw{{d0c__yz_gl_ma0j_wm3z3_g0_o00s}}")