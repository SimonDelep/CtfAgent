# Le texte est: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}
# Peut-être que c'est un message en "leet speak" inversé ou une substitution

# Essayons de remplacer les caractères spéciaux par des lettres
# @ pourrait être 'a', 0 pourrait être 'o', etc.

text = "csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}"

# Remplacements possibles:
# 0 -> o
# @ -> a
# _ -> espace ou underscore
# 3 -> e

decoded = text.replace('0', 'o').replace('@', 'a').replace('3', 'e')
print("Avec substitutions simples:", decoded)

# Essayons aussi d'inverser certaines substitutions
# Peut-être que c'est un message qui a été "leetifié" et qu'il faut le "dleetifier"