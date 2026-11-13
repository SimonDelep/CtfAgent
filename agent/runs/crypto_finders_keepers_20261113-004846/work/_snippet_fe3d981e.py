# La chaîne chiffrée est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Le préfixe attendu est: csaw{

# La clé XOR pour les 5 premiers chars est [6, 0, 15, 7, 0]
# Peut-être que la clé est basée sur une séquence qui change

# Autre idée: peut-être que c'est un XOR avec une clé qui est la somme des positions
# ou un autre motif mathématique

# Regardons les valeurs XOR nécessaires pour chaque position
chiffre = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si on suppose que le flag est csaw{...}, alors:
# pos 0: e -> c, XOR = 6
# pos 1: s -> s, XOR = 0
# pos 2: n -> a, XOR = 15
# pos 3: p -> w, XOR = 7
# pos 4: { -> {, XOR = 0

# Peut-être que la clé est [6, 0, 15, 7, 0] et qu'elle se répète, mais le résultat
# n'est pas tout à fait correct. Peut-être que le flag est en fait ce résultat
# et qu'il faut juste le soumettre tel quel?

# Ou peut-être que la clé change après le préfixe

# Essayons de voir si la clé est basée sur une séquence comme [6, 0, 15, 7, 0, 0, 0, ...]
# c'est-à-dire que seule la clé pour le préfixe est non nulle

cle = [6, 0, 15, 7, 0] + [0] * (len(chiffre) - 5)
resultat = ""
for i, c in enumerate(chiffre):
    k = cle[i]
    resultat += chr(ord(c) ^ k)
print("XOR avec clé [6,0,15,7,0] puis 0:")
print(resultat)

# Ou peut-être que la clé est [6, 0, 15, 7, 0] et qu'elle s'applique seulement aux 5 premiers
# et le reste est en clair?

resultat2 = ""
for i, c in enumerate(chiffre):
    if i < 5:
        k = [6, 0, 15, 7, 0][i]
        resultat2 += chr(ord(c) ^ k)
    else:
        resultat2 += c
print("\nXOR seulement sur les 5 premiers:")
print(resultat2)
