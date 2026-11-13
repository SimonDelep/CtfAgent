# Texte décodé: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Substitution: e->c, s->s, n->a, p->w

# Appliquons la substitution complète
text = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

sub_map = {'e': 'c', 's': 's', 'n': 'a', 'p': 'w'}

result = ""
for c in text:
    if c in sub_map:
        result += sub_map[c]
    else:
        result += c

print(f"Résultat: {result}")

# Remplaçons @ par _
result2 = result.replace('@', '_')
print(f"Avec @ -> _: {result2}")

# Le flag potentiel est: csaw{d0c__yz_gl_ma0j_wm3z3_g0_o00s}
# Mais cela ne semble pas très lisible

# Peut-être que la substitution est différente
# Essayons de voir si c'est une substitution où chaque lettre est décalée
# d'une valeur fixe

# Ou peut-être que c'est une substitution de type "affine cipher"
# où chaque lettre est transformée par une fonction affine

# Pour l'instant, essayons de soumettre le flag avec le message actuel
# et voir si c'est correct

flag = "csaw{d0c__yz_gl_ma0j_wm3z3_g0_o00s}"
print(f"Flag: {flag}")