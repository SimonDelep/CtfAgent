# Analyser la substitution entre le préfixe observé et le préfixe attendu
observed = "esnp"
expected = "csaw"

# Trouver le décalage ou la substitution
for i, (o, e) in enumerate(zip(observed, expected)):
    diff = ord(e) - ord(o)
    print(f"{o} -> {e} : diff = {diff} (ord: {ord(o)} -> {ord(e)})")

# Appliquer la même logique au reste du payload
payload = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Si c'est une substitution monoalphabétique simple, on peut déduire la clé
# esnp -> csaw : e->c, s->s, n->a, p->w
# e(101) -> c(99) : -2
# s(115) -> s(115) : 0
# n(110) -> a(97) : -13
# p(112) -> w(119) : +7

# Ce n'est pas un simple décalage (ROT). C'est une substitution arbitraire.
# Construisons la table de substitution à partir du préfixe
sub_map = {}
for o, e in zip(observed, expected):
    sub_map[o] = e

print(f"Table de substitution déduite du préfixe : {sub_map}")

# Appliquer cette substitution au payload complet
decoded_chars = []
for char in payload:
    if char in sub_map:
        decoded_chars.append(sub_map[char])
    else:
        decoded_chars.append(char)

decoded = ''.join(decoded_chars)
print(f"Payload partiellement décodé : {decoded}")