# Le texte déchiffré avec "cantfind" est: csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}
# Essayons de voir si c'est un message en "leet speak" qui a besoin d'être "dleetifié"

text = "y0u_@lw@el_zu0e_hz3w3_e0_o00f"

# Substitutions courantes en leet speak:
# 0 -> o
# 1 -> i ou l
# 3 -> e
# 4 -> a
# 5 -> s
# 7 -> t
# @ -> a
# _ -> espace ou underscore

# Essayons de remplacer les caractères courants
decoded = text.replace('0', 'o').replace('@', 'a').replace('3', 'e').replace('4', 'a').replace('5', 's').replace('7', 't')
print("Avec substitutions leet:", decoded)

# Peut-être que c'est un message qui a été "leetifié" et qu'il faut le "dleetifier"
# Essayons aussi de voir si c'est un anagramme ou une autre transformation