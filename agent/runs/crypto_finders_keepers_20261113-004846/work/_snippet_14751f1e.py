# Analyser la chaîne chiffrée et tester différentes clés XOR
chiffre = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
attendu = "csaw{...}"

# Clé déduite des 5 premiers caractères
print("Clé XOR déduite (e->c, s->s, n->a, p->w, {->{):")
for i, (c, a) in enumerate(zip(chiffre[:5], "csaw{")):
    print(f"  '{c}' XOR '{a}' = {ord(c) ^ ord(a)}")

# Tester avec "finderskeepers" comme clé
cle = "finderskeepers"
print(f"\nEssai avec clé 'finderskeepers' répété:")
resultat = ""
for i, c in enumerate(chiffre):
    k = cle[i % len(cle)]
    resultat += chr(ord(c) ^ ord(k))
print(resultat)

# Tester avec "finders" comme clé
cle2 = "finders"
print(f"\nEssai avec clé 'finders' répété:")
resultat2 = ""
for i, c in enumerate(chiffre):
    k = cle2[i % len(cle2)]
    resultat2 += chr(ord(c) ^ ord(k))
print(resultat2)

# Tester avec "keepers" comme clé
cle3 = "keepers"
print(f"\nEssai avec clé 'keepers' répété:")
resultat3 = ""
for i, c in enumerate(chiffre):
    k = cle3[i % len(cle3)]
    resultat3 += chr(ord(c) ^ ord(k))
print(resultat3)
