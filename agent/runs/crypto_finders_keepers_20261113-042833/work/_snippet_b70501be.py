# Le XOR avec clé [6, 0, 15, 7] sur "esnp" donne "csaw"
# Donc peut-être que le préfixe est chiffré avec XOR, et le reste est en clair

# Vérifions :
# e ^ 6 = c (101 ^ 6 = 99 = c) ✓
# s ^ 0 = s (115 ^ 0 = 115 = s) ✓
# n ^ 15 = a (110 ^ 15 = 97 = a) ✓
# p ^ 7 = w (112 ^ 7 = 119 = w) ✓

# Donc le préfixe "esnp" XOR [6, 0, 15, 7] = "csaw"
# Et le reste du message est déjà en clair

# Le contenu entre accolades est : d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Peut-être que c'est déjà le message en clair

# Mais attendons, regardons le XOR sur tout le message :
# csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr

# Le } après csaw suggère que l'accolade { a été XORée
# { est ASCII 123, 123 ^ 6 = 125 = }

# Donc le XOR a été appliqué sur tout le message, y compris les accolades
# Mais le résultat n'est pas très lisible

# Peut-être que le XOR ne s'applique que sur les 4 premiers caractères
# Et le reste est en clair

# Donc le flag serait : csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}

# Mais vérifions si le contenu entre accolades a un sens
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print(f"Contenu: {content}")

# Peut-être que @ est un underscore ou un espace
# Essayons de remplacer @ par _
modified = content.replace("@", "_")
print(f"@ -> _: {modified}")

# Ou peut-être que c'est un message en leet speak
# d0c = doc
# @yz = ?yz
# gl = gl
# mn0j = mn0j
# pm3z3 = pm3z3
# g0 = go
# o00s = o00s

# Peut-être que c'est "doc_xyz_gl_mn0j_pm3z3_go_o00s"
# Ou "doc_yz_gl_mn0j_pm3z3_go_o00s"

# Essayons de lire le contenu comme un message en leet speak
# d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# doc_xyz_gl_mn0j_pm3z3_go_o00s

# Peut-être que c'est "doc_xyz_gl_mn0j_pm3z3_go_o00s"
# Et que le flag est csaw{doc_xyz_gl_mn0j_pm3z3_go_o00s}

# Mais d'abord, essayons de soumettre avec le préfixe csaw et le contenu tel quel
print("\nFlag possible: csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}")

# Ou peut-être que le contenu est aussi chiffré
# Essayons de voir si le contenu est un décalage de quelque chose

# Regardons les caractères spéciaux : @, _, 0, 3
# @ est ASCII 64, _ est 95
# Peut-être que @ devrait être un espace ou un autre caractère

# Essayons de remplacer @ par un espace
modified = content.replace("@", " ")
print(f"@ -> espace: {modified}")

# Essayons de remplacer @ par un underscore
modified = content.replace("@", "_")
print(f"@ -> _: {modified}")