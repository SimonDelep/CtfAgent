content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons de remplacer les caractères par des lettres
# d0c -> doc
# @yz -> ? (peut-être "ayz" ou "tyz" ou "ayz")
# gl -> gl
# mn0j -> mnoj (ou mn0j)
# pm3z3 -> pm3z3 (ou pmeze)
# g0 -> go
# o00s -> oos (ou oooos)

# Si on remplace 0->o, 3->e, @->a, _->espace:
# doc ayz a gl mnoj pmeze go oooos
# "doc ayz a gl mnoj pmeze go oooos"

# Peut-être que c'est "doc at zgl mn0j pm3z3 go o00s" ?
# Ou peut-être que c'est un message en français ?

# Essayons de voir si c'est un message en "base64" avec un alphabet personnalisé
# où _ et @ sont des caractères valides

# Autre idée: peut-être que le contenu est déjà le message final, et qu'il faut juste le soumettre ?
# Le problème dit "Submit the decoded plaintext without a flag wrapper"
# Donc peut-être que le "decoded plaintext" est simplement "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" ?

# Mais attendons, le contenu semble encore codé. Peut-être que c'est du "base64" avec un alphabet différent ?
# Ou peut-être que c'est un message en "rot" ou "caesar" cipher appliqué au contenu ?

# Essayons de voir si le contenu est un message en "base64" avec un alphabet personnalisé
# où _ remplace + et @ remplace / (ou l'inverse)

# Essayons de lire le contenu comme un message en "leet speak"
# d0c = doc (document ?)
# @yz = ? 
# gl = ?
# mn0j = ?
# pm3z3 = ?
# g0 = go
# o00s = oos ?

# Peut-être que c'est "doc at zgl mn0j pm3z3 go o00s" et que c'est un message codé ?
# Ou peut-être que le flag est simplement "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" ?

# Essayons de soumettre le contenu tel quel
print("Contenu déchiffré: d0c_@yz@gl_mn0j_pm3z3_g0_o00s")
print("Sans wrapper: d0c_@yz@gl_mn0j_pm3z3_g0_o00s")

# Peut-être que le message est "doc at zgl mn0j pm3z3 go o00s" et qu'il faut le lire comme un message en anglais ?
# "doc at zgl mn0j pm3z3 go o00s" -> "doc at zgl mn0j pm3z3 go o00s"

# Ou peut-être que c'est "doc ayz a gl mnoj pmeze go oooos" ?
# "doc ayz a gl mnoj pmeze go oooos" -> "doc ayz a gl mnoj pmeze go oooos"

# Essayons de voir si c'est un message en "base64" avec un alphabet personnalisé
# où _ et @ sont des caractères valides

# Autre idée: peut-être que le contenu est déjà le message final, et qu'il faut juste le soumettre ?
# Le problème dit "Submit the decoded plaintext without a flag wrapper"
# Donc peut-être que le "decoded plaintext" est simplement "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" ?

# Essayons de soumettre le flag
print("\nFlag possible: csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}")