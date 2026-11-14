ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
content = ciphertext[5:-1]  # d0c_@yz@gl_mn0j_pm3z3_g0_o00s
ciph_letters = [c for c in content if c.isalpha()]
print("Lettres dans le contenu:", ''.join(ciph_letters))
print("Nombre:", len(ciph_letters))

# Essayons différentes hypothèses de texte clair de 15 lettres
# "you_always_be_here" = y o u a l w a y s b e h e r e = 15 lettres
# Mais avec les underscores: y o u _ a l w a y s _ b e _ h e r e = 19 caractères

# Le contenu a des underscores et autres caractères non-alphabétiques
# Content: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Position: 0123456789...

# Les lettres sont aux positions: d(0), c(2), y(5), z(6), g(8), l(9), m(11), n(12), j(14), p(16), m(17), z(19), g(21), o(24), s(27)
# Wait, let me recount
print("\nAnalyse détaillée:")
for i, c in enumerate(content):
    print(f"{i}: {c!r} {'(lettre)' if c.isalpha() else ''}")