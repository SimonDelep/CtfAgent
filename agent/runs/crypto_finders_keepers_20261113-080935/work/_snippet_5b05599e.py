# Analysons la chaîne chiffrée et essayons de trouver la substitution
cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Connaissances partielles :
# e->c, s->s, n->a, p->w (pour esnp -> csaw)
# 0->o
# @->a, y->z, z->u, g->r, l->e (pour @yz@gl -> azure)
# 3->e

# Essayons de déduire le reste
# mn0j -> ?a?o? (n->a, 0->o)
# pm3z3 -> w?eu? (p->w, 3->e, z->u)
# g0 -> ?o (0->o)
# o00s -> o?o? (0->o, s->s) -> oops donc o->o, 0->o, s->s

# Pour o00s -> oops:
# o->o, 0->o, 0->o, s->s
# Donc o->o et 0->o (confiré)

# Pour g0 -> go:
# g->g, 0->o
# Mais plus haut g->r pour azure... contradiction!

# Peut-être que g0 n'est pas "go" mais autre chose
# Ou peut-être que la substitution est différente

# Regardons la structure attendue : csaw{doc_azure_..._go_oops}
# Donc on attend : doc_azure_X_Y_go_oops

# mn0j -> ? -> peut-être "main" ou "manage" ou "manj"
# pm3z3 -> ? -> peut-être "weuse" ou "w3use" ou "w3z3"

# Essayons de trouver une substitution cohérente
# Si mn0j -> "main": m->m, n->a, 0->i? non, 0->o déjà
# Si mn0j -> "manj": m->m, n->a, 0->n? non
# Si mn0j -> "mono": m->m, n->o? non, n->a déjà

# Peut-être que mn0j -> "man0" -> "mano"? 
# Ou mn0j -> "mno0" -> "mnoo"?

# Essayons une approche différente : trouver la substitution complète
# en supposant que le message est lisible

# Connaissances :
# e->c, s->s, n->a, p->w
# 0->o
# @->a, y->z, z->u, g->r, l->e
# 3->e
# o->o (de o00s -> oops)

# Pour mn0j :
# m->?, n->a, 0->o, j->?
# Donc mn0j -> ?a?o?

# Pour pm3z3 :
# p->w, m->?, 3->e, z->u, 3->e
# Donc pm3z3 -> w?eu?

# Pour g0 :
# g->r (de azure), 0->o
# Donc g0 -> ro

# Mais on attend "go" dans la structure... peut-être que c'est "ro"?
# Ou peut-être que g->g pour g0 mais g->r pour azure?

# Attends, peut-être que la substitution n'est pas monoalphabétique
# Ou peut-être que j'ai mal interprété

# Regardons à nouveau : @yz@gl
# @->a, y->z, z->u, @->a, g->r, l->e
# Donc @yz@gl -> a z u a r e -> "azure"

# Et g0 : g->r, 0->o -> "ro"
# Mais on s'attend à "go" dans "csaw{doc_azure_..._go_oops}"

# Peut-être que le mot n'est pas "go" mais "ro"?
# Ou peut-être que g->g dans ce contexte?

# Essayons de trouver ce que pourrait être mn0j et pm3z3
# Si on suppose que le message est en anglais et lisible:
# mn0j -> ?a?o? -> peut-être "mano", "mano", "mano"?
# pm3z3 -> w?eu? -> peut-être "weuse", "w3use", "w3eu3"?

# Essayons de deviner :
# Si mn0j -> "mano" : m->m, n->a, 0->n? non, 0->o déjà
# Si mn0j -> "mano" : m->m, n->a, 0->o, j->? -> "mao?"
# Si j->n, alors mn0j -> "mano" -> "mano"

# Si pm3z3 -> "weuse" : p->w, m->e? non, m->?, 3->e, z->u, 3->e
# Donc pm3z3 -> w?eu?
# Si m->s, alors pm3z3 -> "wseue" -> pas "weuse"
# Si m->u, alors pm3z3 -> "wueue" -> pas "weuse"

# Peut-être que pm3z3 -> "w3eu3" -> "w3eu3"?
# Ou pm3z3 -> "w3z3" -> "w3z3"?

# Essayons une autre approche : utiliser substitution_solver
print("Analyse de la substitution:")
print(f"Chiffre: {cipher}")

# Table de substitution connue partiellement
sub_known = {
    'e': 'c', 's': 's', 'n': 'a', 'p': 'w',
    '0': 'o', '@': 'a', 'y': 'z', 'z': 'u', 'g': 'r', 'l': 'e',
    '3': 'e', 'o': 'o'
}

# Appliquons la substitution connue
decoded = ""
for char in cipher:
    if char in sub_known:
        decoded += sub_known[char]
    else:
        decoded += char

print(f"Décode partiel: {decoded}")

# Maintenant, essayons de trouver les lettres manquantes
# Les lettres inconnues dans le chiffrement sont: d, c, _, m, j, (et peut-être d'autres)
# Dans decoded, on a: csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Après substitution partielle: csaw{doc_azure_ma0j_we3z3_ro_oops}

# Attends, recalculons:
# e->c, s->s, n->a, p->w
# 0->o, @->a, y->z, z->u, g->r, l->e, 3->e, o->o

# esnp -> csaw (correct)
# d0c -> d o c -> "doc" (d et c inconnus, mais on suppose d->d, c->c)
# @yz@gl -> a z u a r e -> "azure"
# mn0j -> m a o j -> "maoj" (m et j inconnus)
# pm3z3 -> w m e u e -> "wmeue" (m inconnu)
# g0 -> r o -> "ro"
# o00s -> o o o s -> "ooos" -> mais on attend "oops"

# Attends, o00s: o->o, 0->o, 0->o, s->s -> "ooos"
# Mais on s'attend à "oops", donc o->o, 0->o, 0->p? non, 0->o déjà
# Donc o00s -> "ooos" mais on attend "oops"

# Il y a une incohérence. Peut-être que 0->o et le deuxième 0->p?
# Ou peut-être que la substitution n'est pas monoalphabétique

# Re-examinons o00s -> oops:
# o->o, 0->o, 0->p, s->s -> "oops"
# Donc le deuxième 0->p? Mais le premier 0->o?
# C'est contradictoire pour une substitution monoalphabétique

# Peut-être que o00s n'est pas "oops" mais "ooos"?
# Ou peut-être que la chaîne chiffrée est différente

# Laissons le code afficher le résultat partiel
print(f"Substitution connue: {sub_known}")