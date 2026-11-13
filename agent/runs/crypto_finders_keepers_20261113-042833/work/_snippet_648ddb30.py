# "esnp" pourrait être un anagramme de "pens" (pensées) ou "spen"
# Ou peut-être que c'est "csaw" avec un décalage différent

# Regardons les XOR à nouveau : 6, 0, 15, 7
# 6 = 0x06, 0 = 0x00, 15 = 0x0F, 7 = 0x07

# Peut-être que c'est une clé XOR qui se répète
# Essayons de XORer tout le message avec une clé basée sur ces valeurs

encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7]

# XOR sur tous les caractères
decoded = ""
for i, c in enumerate(encrypted):
    decoded += chr(ord(c) ^ key[i % len(key)])
print(f"XOR avec clé {key}: {decoded}")

# Peut-être que c'est un décalage sur les lettres seulement
# Mais avec une clé différente

# Essayons de voir si le contenu entre accolades est un mot lisible
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print(f"\nContenu: {content}")

# Peut-être que @ est un espace ou un underscore
# Et que c'est un message en leet speak

# d0c -> doc
# @yz -> ?yz
# gl -> gl
# mn0j -> mn0j
# pm3z3 -> pm3z3
# g0 -> go
# o00s -> o00s

# Peut-être que c'est "doc_xyz_gl_mn0j_pm3z3_go_o00s"
# Ou "doc_yz_gl_mn0j_pm3z3_go_o00s"

# Essayons de remplacer @ par un underscore
modified = content.replace("@", "_")
print(f"@ -> _: {modified}")

# Essayons de remplacer @ par un espace
modified = content.replace("@", " ")
print(f"@ -> espace: {modified}")

# Peut-être que c'est un message en leet speak
# d0c = doc
# @yz = ?yz (peut-être "xyz" ou "ayz")
# gl = gl (good luck?)
# mn0j = mn0j (manoj? monj?)
# pm3z3 = pm3z3 (pmez3? pm3z3)
# g0 = go
# o00s = o00s (oos? ooss?)

# Essayons de lire le contenu comme un message en leet speak
# d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# doc_xyz_gl_mn0j_pm3z3_go_o00s

# Peut-être que c'est "doc_xyz_gl_mn0j_pm3z3_go_o00s"
# Et que le flag est csaw{doc_xyz_gl_mn0j_pm3z3_go_o00s}

# Mais attendons, peut-être que le préfixe "esnp" est correct
# Et que le flag est esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}

print("\nFlag possible: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}")
print("Ou: csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}")