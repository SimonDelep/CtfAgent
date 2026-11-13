# Comparons les lettres pour trouver la substitution
encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw{"

# e -> c : e(4) -> c(2) = -2
# s -> s : s(18) -> s(18) = 0
# n -> a : n(13) -> a(0) = -13 ou +13
# p -> w : p(15) -> w(22) = +7

# Ce n'est pas un simple décalage constant. Essayons de voir si c'est un Atbash ou autre
# Atbash: a<->z, b<->y, etc.
# e -> v (pas c)
# s -> h (pas s)

# Peut-être un chiffrement Vigenère avec une clé ?
# Ou une substitution basée sur une table spécifique

# Regardons les positions ASCII
print("Analyse des positions:")
for i, (enc, exp) in enumerate(zip(encoded[:5], expected_prefix)):
    if enc.isalpha() and exp.isalpha():
        diff = ord(enc) - ord(exp)
        print(f"  {enc} -> {exp}: diff = {diff}")

# Essayons de voir si c'est un chiffrement affine
# Pour e->c: (a*4 + b) mod 26 = 2
# Pour s->s: (a*18 + b) mod 26 = 18
# Pour n->a: (a*13 + b) mod 26 = 0
# Pour p->w: (a*15 + b) mod 26 = 22

# De s->s: a*18 + b = 18 mod 26
# De e->c: a*4 + b = 2 mod 26
# Soustraction: a*14 = 16 mod 26
# a = 16/14 mod 26... 14 et 26 ne sont pas premiers entre eux, donc plusieurs solutions

# Essayons de trouver a et b
for a in range(1, 26):
    for b in range(26):
        if (a*4 + b) % 26 == 2 and (a*18 + b) % 26 == 18:
            # Vérifions avec n->a
            if (a*13 + b) % 26 == 0:
                # Vérifions avec p->w
                if (a*15 + b) % 26 == 22:
                    print(f"Solution affine trouvée: a={a}, b={b}")

# Si pas de solution affine, essayons autre chose
print("\nEssayons de décoder avec différentes substitutions:")

# Peut-être que c'est un ROT avec une clé différente pour chaque lettre ?
# Ou un chiffrement par transposition ?

# Regardons le contenu complet
print(f"\nMessage complet: {encoded}")
print(f"Après substitution partielle (e->c, n->a, p->w, @->_):")
sub = {'e': 'c', 'n': 'a', 'p': 'w', '@': '_', 's': 's'}
decoded = ''.join(sub.get(c, c) for c in encoded)
print(f"  {decoded}")

# Le contenu entre accolades: d0c__yz_gl_ma0j_wm3z3_g0_o00s
# Peut-être que c'est un mot ou une phrase ?
content = "d0c__yz_gl_ma0j_wm3z3_g0_o00s"
print(f"\nAnalyse du contenu: {content}")

# Essayons de voir si c'est un mot avec des chiffres qui remplacent des lettres
# d0c pourrait être "doc" ou "dec"
# yz pourrait être... ?
# gl pourrait être... ?

# Peut-être que c'est "doc_xyz_gl_ma0j_wm3z3_g0_o00s"
# Et que xyz est un mot ?

# Essayons de deviner le mot complet en cherchant des patterns
# "d0c" -> "doc" (d->d, 0->o, c->c) - mais 0 est déjà un chiffre
# Attends, peut-être que 0 = o ?

# Regardons: d0c -> doc si 0=o
# Mais dans le message original, on a d0c, pas doc
# Donc peut-être que le chiffre 0 représente la lettre o ?

# Essayons de remplacer 0 par o
content2 = content.replace('0', 'o')
print(f"Avec 0->o: {content2}")

# d0c -> doc
# ma0j -> maoj ?
# wm3z3 -> wm3z3
# g0 -> go
# o00s -> o00s -> ooss ?

# Hmm, peut-être que c'est un mot technique ?
# "doc_xyz_gl_maoj_wm3z3_go_ooss"

# Essayons de voir si c'est un anagramme ou quelque chose comme ça
# Ou peut-être que c'est un mot en anglais avec des chiffres pour des lettres similaires (leetspeak)

# Leetspeak courant:
# 0 = o
# 3 = e
# 1 = l ou i
# 4 = a
# 5 = s
# 7 = t

# Appliquons le leetspeak inverse
leetspeak_map = {'0': 'o', '3': 'e', '1': 'l', '4': 'a', '5': 's', '7': 't'}
decoded_leet = ""
for c in content:
    decoded_leet += leetspeak_map.get(c, c)
print(f"Avec leetspeak inverse: {decoded_leet}")
