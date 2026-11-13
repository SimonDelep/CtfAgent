# Texte décodé: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Essayons de comprendre la substitution

# Si e->c, s->s, n->a, p->w, alors quelle est la règle?
# Peut-être que c'est une substitution où chaque lettre est décalée d'une valeur fixe
# mais avec une exception pour certaines lettres?

# Ou peut-être que c'est une substitution basée sur la position dans l'alphabet
# e=4, c=2 -> -2
# s=18, s=18 -> 0
# n=13, a=0 -> -13
# p=15, w=22 -> +7

# C'est très incohérent. Peut-être que c'est une substitution Atbash modifiée?

# Essayons de voir si c'est une substitution où chaque lettre est remplacée par sa
# correspondante dans un alphabet mélangé

# Autre idée: peut-être que le texte est déjà correct et qu'il faut juste
# appliquer une substitution pour obtenir le flag final

# Regardons le texte: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Si on remplace @ par _, on obtient: esnp{d0c__yz_gl_mn0j_pm3z3_g0_o00s}

# Essayons de trouver une substitution qui transforme esnp en csaw
# et qui donne un message lisible

text = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Remplaçons @ par _
text2 = text.replace('@', '_')
print(f"Avec @ -> _: {text2}")

# Maintenant, essayons de trouver la substitution
# e->c, s->s, n->a, p->w

# Si on applique cette substitution à tout le texte:
# e->c, s->s, n->a, p->w, et pour les autres lettres?

# Peut-être que c'est une substitution où chaque lettre est décalée de -2
# e(4) -> c(2) : -2
# s(18) -> q(16) : -2 (mais on veut s->s)

# Attends, peut-être que s->s est une coïncidence et que la règle est différente

# Essayons de voir si c'est une substitution où chaque lettre est remplacée
# par la lettre à la même position dans un alphabet inversé ou mélangé

# Autre idée: peut-être que c'est une substitution de type "keyed cipher"
# où l'alphabet est mélangé selon une clé

# Pour l'instant, essayons de voir si le message a du sens avec une substitution simple
# en supposant que e->c, s->s, n->a, p->w

# Construisons une table de substitution partielle
sub_map = {'e': 'c', 's': 's', 'n': 'a', 'p': 'w'}

# Appliquons cette substitution
result = ""
for c in text:
    if c in sub_map:
        result += sub_map[c]
    else:
        result += c

print(f"Substitution partielle: {result}")

# Maintenant, essayons de deviner la substitution complète
# en supposant que le résultat est un message lisible en anglais

# Le résultat partiel est: csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}
# On voit que "csaw{" est correct, mais le reste n'est pas lisible

# Peut-être que @ est un espace ou un underscore
# Et que les autres lettres ont aussi une substitution

# Essayons de voir si c'est une substitution où chaque lettre est décalée
# d'une valeur qui dépend de sa position

# Ou peut-être que c'est une substitution simple où chaque lettre est remplacée
# par une autre lettre de manière cohérente

# Pour trouver la substitution complète, on peut essayer de deviner le message
# en supposant que c'est un message en anglais

# Le message entre accolades est: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Si on remplace @ par _, on obtient: d0c__yz_gl_mn0j_pm3z3_g0_o00s

# Essayons de voir si c'est un message comme "doc_xyz_gl_mn0j_pm3z3_g0_o00s"
# ou quelque chose comme ça

# En fait, regardons le texte original décodé: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Si on applique e->c, s->s, n->a, p->w, on obtient:
# csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}

# Maintenant, si on suppose que la substitution est cohérente,
# on peut essayer de deviner les autres correspondances

# Par exemple, si d->d (inchangé), c->c (inchangé), etc.
# Mais alors le message ne serait pas lisible

# Peut-être que la substitution est:
# e->c, s->s, n->a, p->w, et pour les autres lettres?

# Essayons de voir si c'est une substitution où chaque lettre est décalée
# d'une valeur fixe, mais avec une exception pour certaines lettres

# Ou peut-être que c'est une substitution de type "affine cipher"
# où chaque lettre est transformée par une fonction affine

# Pour l'instant, essayons de soumettre le flag avec la substitution partielle
# et voir si c'est correct

print()
print("Flag potentiel avec substitution partielle:")
print(f"csaw{{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}}")