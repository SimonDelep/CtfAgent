# Analysons le flag décodé plus en détail
encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Substitution connue : e->c, s->s, n->a, p->w
# @ semble être _
substitution = {'e': 'c', 's': 's', 'n': 'a', 'p': 'w', '@': '_'}

decoded = ""
for c in encoded:
    decoded += substitution.get(c, c)

print(f"Encoded:   {encoded}")
print(f"Decoded:   {decoded}")
print()

# Essayons de voir si c'est un ROT sur les lettres restantes
# Regardons les lettres non-substituées dans le contenu
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print("Analyse des lettres restantes:")
for c in content:
    if c.isalpha():
        print(f"  {c} -> ?")

# Essayons ROT13 sur le contenu
import codecs
rot13 = codecs.encode(content, 'rot_13')
print(f"\nROT13 du contenu: {rot13}")

# Essayons de trouver un pattern
# Peut-être que c'est un mot spécifique ?
# "d0c" pourrait être "doc"
# "yz" pourrait être... ?
# "gl" pourrait être... ?

# Essayons de deviner le mot complet
# csaw{...} - peut-être un mot technique ?
# "doc_xyz_gl_ma0j_wm3z3_g0_o00s"

# Cherchons des patterns dans les chiffres
print("\nChiffres dans le contenu:")
for i, c in enumerate(content):
    if c.isdigit():
        print(f"  position {i}: {c}")
