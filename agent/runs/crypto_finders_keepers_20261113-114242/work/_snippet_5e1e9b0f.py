# Le flag partiel après base64
partial = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("Base64 décodé:", partial)

# Mapping connu:
# e->c, s->a, n->s, p->w
# 0->o, @->_
# Donc: csaw{doc__yz_gl_mnoj_pmeze_go_ooos}

# Essayons de deviner les lettres manquantes
# Pattern: csaw{doc__yz_gl_mnoj_pmeze_go_ooos}
# Les underscores doubles semblent étranges...

# Peut-être que @ n'est pas _ mais une lettre ?
# Et 0 n'est pas toujours o ?

# Regardons les patterns de mots:
# d0c -> doc (0=o)
# g0 -> go (0=o)
# o00s -> ooss ou o00s ?

# Essayons de trouver des mots anglais qui correspondent:
# _yz_ -> ?yz? 
# gl -> gl (gl? maybe "gl" est correct)
# mn0j -> mnoj ou manj ?
# pm3z3 -> pmeze ou pme3e ?

# Peut-être que c'est un message en français ?
# "doc" pourrait être "doc" (document)
# "go" pourrait être "go"

# Essayons une substitution complète avec substitution_solver
payload = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("\nPayload à décoder:", payload)